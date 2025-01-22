# ONLY FOR TESTING WITHOUT DOCKER
import utils

# species	island	bill_length_mm	bill_depth_mm	flipper_length_mm	body_mass_g	sex
# 0	Adelie	Torgersen	39.1	18.7	181.0	3750.0	Male
# 1	Adelie	Torgersen	39.5	17.4	186.0	3800.0	Female
# species	island	bill_length_mm	bill_depth_mm	flipper_length_mm	body_mass_g	sex
# 214	Gentoo	Biscoe	46.1	13.2	211.0	4500.0	Female
# 215	Gentoo	Biscoe	50.0	16.3	230.0	5700.0	Male
# species	island	bill_length_mm	bill_depth_mm	flipper_length_mm	body_mass_g	sex
# 146	Chinstrap	Dream	46.5	17.9	192.0	3500.0	Female
# 147	Chinstrap	Dream	50.0	19.5	196.0	3900.0	Male

print(utils.predict("Torgersen", 39.1, 18.7, 181.0, 3750.0, "Male"))
print(utils.predict("Torgersen", 39.5, 17.4, 186.0, 3800.0, "Female"))
print(utils.predict("Biscoe", 46.1, 13.2, 211.0, 4500.0, "Female"))
print(utils.predict("Biscoe", 50.0, 16.3, 230.0, 5700.0, "Male"))
print(utils.predict("Dream", 46.5, 17.9, 192.0, 3500.0, "Female"))
print(utils.predict("Dream", 50.0, 19.5, 196., 3900.0, "Male"))