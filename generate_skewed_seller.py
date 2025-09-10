import numpy as np
import argparse

def generate_sellers(num_vectors, output_file, seed=42):
    """
    Generate seller assignments for vectors based on the experimental setup:
    - With probability 0.9: assign color from {1, 2, 3} uniformly at random
    - With probability 0.1: assign color from {4, ..., 1000} uniformly at random
    """
    np.random.seed(seed)
    
    sellers = []
    
    for i in range(num_vectors):
        # Generate random number to decide which distribution to use
        prob = np.random.random()
        
        if prob < 0.9:
            # Select from dominant colors {1, 2, 3} uniformly
            seller = np.random.randint(1, 4)  # 1, 2, or 3
        else:
            # Select from {4, ..., 1000} uniformly
            seller = np.random.randint(4, 1001)  # 4 to 1000
        
        sellers.append(seller)
    
    # Write to file
    with open(output_file, 'w') as f:
        for seller in sellers:
            f.write(f"{seller}\n")
    
    print(f"Generated {num_vectors} seller assignments")
    print(f"Saved to: {output_file}")
    
    # Print statistics
    unique_sellers = np.unique(sellers)
    print(f"Number of unique sellers: {len(unique_sellers)}")
    print(f"Seller distribution:")
    for seller_id in [1, 2, 3]:
        count = sellers.count(seller_id)
        print(f"  Seller {seller_id}: {count} vectors ({count/num_vectors*100:.2f}%)")
    
    # Count sellers in range 4-1000
    high_sellers = [s for s in sellers if s >= 4]
    print(f"  Sellers 4-1000: {len(high_sellers)} vectors ({len(high_sellers)/num_vectors*100:.2f}%)")

def generate_sift_sellers(num_vectors, output_file, seed=42):
    """
    Generate seller assignments for SIFT dataset variant:
    - With probability 0.8: assign dominant color (1)
    - With probability 0.2: assign color from {2, ..., 1000} uniformly at random
    """
    np.random.seed(seed)
    
    sellers = []
    
    for i in range(num_vectors):
        # Generate random number to decide which distribution to use
        prob = np.random.random()
        
        if prob < 0.8:
            # Assign dominant color
            seller = 1
        else:
            # Select from {2, ..., 1000} uniformly
            seller = np.random.randint(2, 1001)  # 2 to 1000
        
        sellers.append(seller)
    
    # Write to file
    with open(output_file, 'w') as f:
        for seller in sellers:
            f.write(f"{seller}\n")
    
    print(f"Generated {num_vectors} SIFT-style seller assignments")
    print(f"Saved to: {output_file}")
    
    # Print statistics
    unique_sellers = np.unique(sellers)
    print(f"Number of unique sellers: {len(unique_sellers)}")
    print(f"Seller distribution:")
    
    dominant_count = sellers.count(1)
    print(f"  Dominant seller (1): {dominant_count} vectors ({dominant_count/num_vectors*100:.2f}%)")
    
    # Count sellers in range 2-1000
    other_sellers = [s for s in sellers if s >= 2]
    print(f"  Other sellers (2-1000): {len(other_sellers)} vectors ({len(other_sellers)/num_vectors*100:.2f}%)")

def main():
    parser = argparse.ArgumentParser(description='Generate seller file for diverse search experiments')
    parser.add_argument('--num_vectors', type=int, required=True, 
                       help='Number of vectors in the dataset')
    parser.add_argument('--output_file', type=str, required=True,
                       help='Output file path for seller assignments')
    parser.add_argument('--variant', choices=['original', 'sift'], default='sift',
                       help='Variant to use: original (0.9/0.1 split) or sift (0.8/0.2 split)')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed for reproducibility')
    
    args = parser.parse_args()
    
    if args.variant == 'original':
        generate_sellers(args.num_vectors, args.output_file, args.seed)
    else:
        generate_sift_sellers(args.num_vectors, args.output_file, args.seed)

if __name__ == "__main__":
    main()