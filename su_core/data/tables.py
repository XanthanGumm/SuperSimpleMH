import os
import pathlib
import pandas as pd

root = pathlib.Path(__file__)
while root.name != "SuperSimpleMH":
    root = root.parent

strings = pd.read_csv(os.path.join(root, "resources", "datatables", "strings.csv"))
strings = strings.set_index("key")

statscost = pd.read_csv(
    os.path.join(root, "resources", "datatables", "statscost.csv"),
    dtype={"ValShift": "Int32"},
)
statscost = statscost.set_index("Stat")

runewords = pd.read_csv(os.path.join(root, "resources", "datatables", "runewords.csv"))
runewords = runewords.set_index("ID")

uniques = pd.read_csv(os.path.join(root, "resources", "datatables", "uniqueitems.csv"))
uniques = uniques.set_index("*ID")

sets = pd.read_csv(os.path.join(root, "resources", "datatables", "setitems.csv"))
sets = sets.set_index("*ID")

defensive = pd.read_csv(os.path.join(root, "resources", "datatables", "defensive.csv"))
defensive = defensive.set_index("code")

offensive = pd.read_csv(os.path.join(root, "resources", "datatables", "offensive.csv"))
offensive = offensive.set_index("code")

misc = pd.read_csv(os.path.join(root, "resources", "datatables", "misc.csv"))
misc = misc.set_index("code")

charstats = pd.read_csv(os.path.join(root, "resources", "datatables", "charstats.csv"))
charstats = charstats.set_index("class")

magicprefix = pd.read_csv(os.path.join(root, "resources", "datatables", "magicprefix.csv"))
magicprefix = magicprefix.set_index("ID")

magicsuffix = pd.read_csv(os.path.join(root, "resources", "datatables", "magicsuffix.csv"))
magicsuffix = magicsuffix.set_index("ID")

rareprefix = pd.read_csv(os.path.join(root, "resources", "datatables", "rareprefix.csv"))
rareprefix = rareprefix.set_index("ID")

raresuffix = pd.read_csv(os.path.join(root, "resources", "datatables", "raresuffix.csv"))
raresuffix = raresuffix.set_index("ID")
