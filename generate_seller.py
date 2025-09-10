import random

random.seed(42)
num_points = 1000000  # SIFT1M has 1M points
seller_ids = [random.randint(0, 9) for _ in range(num_points)]
with open('sift_sellers.txt', 'w') as f:
    for seller_id in seller_ids:
        f.write(f'{seller_id}\n')
print('Generated seller file with 10 colors (0-9)')