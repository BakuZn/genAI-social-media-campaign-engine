import pandas as pd
import os
import re

def clean_text(text):
    if pd.isna(text):
        return ""
    # Convert to string, replace non-breaking spaces and newline characters, strip trailing commas
    t = str(text).replace('\xa0', ' ').replace('\n', ' ').strip()
    t = t.rstrip(',')
    # specific normalizations
    t = re.sub(r'UP\s*&\s*UK', 'UP & UK', t, flags=re.IGNORECASE)
    t = re.sub(r'^UP$', 'UP & UK', t, flags=re.IGNORECASE) # group UP with UP & UK based on regions
    return t.strip()

def extract_nested_options(excel_path, output_path):
    print(f"Reading {excel_path}...")
    xls = pd.ExcelFile(excel_path)
    
    # Dictionaries to hold nested relationships
    # state -> set(regions)
    # region -> set(territories)
    state_to_regions = {}
    region_to_territories = {}
    
    crops = set()
    seed_products = set()
    cp_products = set()
    
    cp_columns = ['Nursery', 'Planting', 'Growth', 'Flowering', 'Fruiting', 'Harvest', 'Cupping', 'Early Heading']
    
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Crop logic
        if 'Crop' in df.columns:
            for c in df['Crop'].dropna():
                crops.add(clean_text(c))
        else:
            crops.add(clean_text(sheet_name))
            
        # Seed Products
        if 'Variety' in df.columns:
            for v in df['Variety'].dropna():
                seed_products.add(clean_text(v))
                
        # CP Products
        for col in cp_columns:
            if col in df.columns:
                for p in df[col].dropna():
                    cleaned_p = clean_text(p)
                    if cleaned_p:
                        cp_products.add(cleaned_p)
                        
        # Hierarchy extraction
        for _, row in df.iterrows():
            state = clean_text(row.get('State', ''))
            region = clean_text(row.get('Region', ''))
            territory = clean_text(row.get('Territory', ''))
            
            if state:
                if state not in state_to_regions:
                    state_to_regions[state] = set()
                if region:
                    state_to_regions[state].add(region)
                    
            if region:
                if region not in region_to_territories:
                    region_to_territories[region] = set()
                if territory:
                    region_to_territories[region].add(territory)

    # Write to file hierarchically
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=== NESTED GEOGRAPHY (For MS Forms Branching) ===\n\n")
        f.write("To implement 'nested' options in MS Forms, you must use Branching.\n")
        f.write("Create a section for each State. If a user selects 'Maharashtra', branch them to the 'Maharashtra' section to choose Regions/Territories.\n\n")
        
        for state in sorted(state_to_regions.keys()):
            f.write(f"STATE: {state}\n")
            regions = sorted(list(state_to_regions[state]))
            if not regions:
                f.write("  (No regions listed)\n")
            for region in regions:
                f.write(f"  └── REGION: {region}\n")
                territories = sorted(list(region_to_territories.get(region, set())))
                # Remove empty territories
                territories = [t for t in territories if t]
                if territories:
                    for t in territories:
                        f.write(f"      └── TERRITORY: {t}\n")
                else:
                    f.write("      └── (No territories listed)\n")
            f.write("\n")
            
        f.write("\n=========================================\n")
        f.write("=== FLAT LISTS (For standard questions) ===\n")
        f.write("=========================================\n\n")
        
        f.write("=== ALL CROPS ===\n")
        f.write("\n".join(sorted([c for c in crops if c])) + "\n\n")
        
        f.write("=== ALL SEED PRODUCTS (Varieties) ===\n")
        f.write("\n".join(sorted([s for s in seed_products if s])) + "\n\n")
        
        f.write("=== ALL CP PRODUCTS ===\n")
        f.write("\n".join(sorted([p for p in cp_products if p])) + "\n\n")

    print(f"Successfully extracted accurate nested options to {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    excel_file = os.path.join(base_dir, "crop calendar.xlsx")
    output_file = os.path.join(base_dir, "ms_forms_dropdowns.txt")
    
    extract_nested_options(excel_file, output_file)
