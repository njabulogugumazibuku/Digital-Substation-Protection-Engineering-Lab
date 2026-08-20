import math

# ==========================================
# DIGITAL SUBSTATION PROTECTION ENGINEERING LAB
# Rated Current Calculations
# ==========================================

# Transformer parameters
transformer_rating_mva = 50
hv_voltage_kv = 132
lv_voltage_kv = 33

# Convert units
transformer_rating_va = transformer_rating_mva * 1_000_000
hv_voltage_v = hv_voltage_kv * 1_000
lv_voltage_v = lv_voltage_kv * 1_000

# Three-phase rated current calculation
# I = S / (sqrt(3) × V)

hv_rated_current = transformer_rating_va / (
    math.sqrt(3) * hv_voltage_v
)

lv_rated_current = transformer_rating_va / (
    math.sqrt(3) * lv_voltage_v
)

print("TRANSFORMER RATED CURRENT CALCULATIONS")
print("-" * 45)

print(
    f"Transformer Rating: "
    f"{transformer_rating_mva} MVA"
)

print(
    f"HV Rated Current: "
    f"{hv_rated_current:.2f} A"
)

print(
    f"LV Rated Current: "
    f"{lv_rated_current:.2f} A"
)

# ==========================================
# Maximum Operating Current Assumption
# ==========================================

continuous_loading_factor = 1.20

hv_max_operating_current = (
    hv_rated_current * continuous_loading_factor
)

lv_max_operating_current = (
    lv_rated_current * continuous_loading_factor
)

print("\nMAXIMUM OPERATING CURRENT")
print("-" * 45)

print(
    f"HV Maximum Operating Current: "
    f"{hv_max_operating_current:.2f} A"
)

print(
    f"LV Maximum Operating Current: "
    f"{lv_max_operating_current:.2f} A"
)
