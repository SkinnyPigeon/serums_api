from sqlalchemy import create_engine
import os
import subprocess
import pandas as pd
from pdf2image import convert_from_path
from PIL import Image
import base64


project_folder = subprocess.check_output("pwd", shell=True).\
                            decode("utf-8").rstrip()

PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')
ALCHEMY_USER = os.getenv('ALCHEMY_USER')

engine = create_engine(
    f'postgresql://{ALCHEMY_USER}:{PASSWORD}@localhost:{PORT}/source'
)

image_path = f"{project_folder}api/databases/data/zmc/images"

print("Converting Hip Image")
with open(f"{image_path}/hip.png".format(image_path=image_path), "rb") as i:
    image_1 = str(base64.b64encode(i.read())).\
        replace("b'", "").\
        replace("'", "")

print("Converting Pelvis Image")
with open(f"{image_path}/pelvis.png".format(image_path=image_path), "rb") as i:
    image_2 = str(base64.b64encode(i.read())).\
        replace("b'", "").\
        replace("'", "")

print("Converting orthopedics report")
doc_path = f"{project_folder}api/databases/data/zmc/documents"
doc1 = convert_from_path(
    f"{doc_path}/2020.02.14 Resultaten verwijzing orthopedisch onderzoek.pdf",
    500
)

for i in range(len(doc1)):
    doc1[i].save(f'{doc_path}/converted/page' + str(i) + '.png', 'PNG')
    page_img = Image.open(f'{doc_path}/converted/page' + str(i) + '.png')
    if i == 0:
        img = Image.new('RGB', (page_img.width, page_img.height * len(doc1)))
    img.paste(page_img, (0, page_img.height * i))
    os.remove(f'{doc_path}/converted/page' + str(i) + '.png')

img.save(f'{doc_path}/converted/concat.png', 'PNG')
with open(f'{doc_path}/converted/concat.png', "rb") as image_file:
    document1 = str(base64.b64encode(image_file.read())).\
        replace("b'", "").\
        replace("'", "")

print("Converting operation report")
doc2 = convert_from_path(
    f"{doc_path}/2020.03.16 Operatieraport "
    "vervanging rechter heupgewricht.pdf",
    500
)
for i in range(len(doc2)):
    doc2[i].save(f'{doc_path}/converted/page' + str(i) + '.png', 'PNG')
    page_img = Image.open(f'{doc_path}/converted/page' + str(i) + '.png')
    if i == 0:
        img = Image.new('RGB', (page_img.width, page_img.height * len(doc2)))
    img.paste(page_img, (0, page_img.height * i))
    os.remove(f'{doc_path}/converted/page' + str(i) + '.png')

img.save(f'{doc_path}/converted/concat.png', 'PNG')
with open(f'{doc_path}/converted/concat.png', "rb") as image_file:
    document2 = str(base64.b64encode(image_file.read())).\
        replace("b'", "").\
        replace("'", "")

# Saving to database

patient_details = pd.read_csv(
    f"{project_folder}api/databases/data/zmc/patient_details.csv"
)

patnr_list = list(set(patient_details['patnr']))
patnr_count = len(patnr_list)
full_patnr_list = patnr_list + patnr_list

rhx = ['Right hip x-ray' for _ in range(patnr_count)]
rpx = ['Right pelvis x-ray' for _ in range(patnr_count)]
x_ray_list = rhx + rpx
x_types = ['x-ray' for _ in range(2 * patnr_count)]
x_ray_dates = ['2020-09-01' for _ in range(2 * patnr_count)]
rhi = [image_1 for _ in range(patnr_count)]
rpi = [image_2 for _ in range(patnr_count)]
x_ray_images = rhi + rpi


dt1 = ['Resultaten verwijzing orthopedisch onderzoek'
       for _ in range(patnr_count)]
dt2 = ['Operatieraport vervanging rechter heupgewricht'
       for _ in range(patnr_count)]
document_list = dt1 + dt2
d_types = ['orthopedics' for _ in range(2 * patnr_count)]
dd1 = ['2020.02.14' for _ in range(patnr_count)]
dd2 = ['2020.03.16' for _ in range(patnr_count)]
document_dates = dd1 + dd2
doc1 = [document1 for _ in range(patnr_count)]
doc2 = [document2 for _ in range(patnr_count)]
document_list = doc1 + doc2

images = {
    'patnr': full_patnr_list,
    'image_title': x_ray_list,
    'type': x_types,
    'date': x_ray_dates,
    'image': x_ray_images
}
documents = {
    'patnr': full_patnr_list,
    'document_title': document_list,
    'type': d_types,
    'date': document_dates,
    'document': document_list
}

image_df = pd.DataFrame.from_dict(images)
document_df = pd.DataFrame.from_dict(documents)

print("Saving images")
image_df.to_sql(
    'images',
    con=engine,
    if_exists='append',
    index=False,
    schema='zmc'
)

print("Saving documents")
document_df.to_sql(
    'documents',
    con=engine,
    if_exists='append',
    index=False,
    schema='zmc'
)

engine.dispose()
print("FINISHED CONVERTING AND SAVING FILES")
