import seaborn as sns
import matplotlib.pyplot as plt
import json

# 두 변수는 각자 데이터 경로에 따라 변경 필요
dataset_dir = "./coco/"
train_json_dir = dataset_dir + "coco_1.json"

# COCO json 파일 읽기
with open(train_json_dir, 'r') as f:
    coco_json = json.load(f)

images = coco_json['images']
categories = coco_json['categories']
annotations = coco_json['annotations']
categories_names = ['None','PET','PS','PP','PE', 'None']    # 모든 품목 출력

sns.set(rc = {'figure.figsize':(8,5)})
fig, ax1 = plt.subplots() # ax1: bounding box

# 카테고리별 bounding box 개수를 카테고리 이름과 함께 저장
category_to_num_bbox = []
for i, category_name in enumerate(categories_names):
    if i == 0:
        continue  # 'None'은 제외
    num_bbox = sum([ann['category_id'] == i for ann in annotations])
    category_to_num_bbox.append((category_name, num_bbox))

# category_to_area_bbox: 카테고리별 bouning box 면적정보를 리스트형태로 저장
category_to_area_bbox = [[] for i in range(len(categories_names))]
for annotation in annotations:
    category = annotation['category_id']
    bbox = annotation['bbox']
    area = annotation['area']
    category_to_area_bbox[category].append(area)

# 카테고리별 bounding box 면적 분포를 kdeplot으로 시각화
for idx_category in range(1, len(category_to_num_bbox)):
    sns.kdeplot(category_to_area_bbox[idx_category], label=categories_names[idx_category], ax=ax1)

plt.rc('legend', fontsize=15)
ax1.legend()
ax1.set_title("Area distribution of bounding box per category", fontsize=15)
ax1.set_xlabel("Area", fontsize=15)
plt.ylim([0, (1e-5)/0.1])
plt.show()
print(category_to_area_bbox)