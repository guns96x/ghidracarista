from androguard.core.dex import DEX
import re

with open(r"d:\ghidracarista\extracted\base\classes.dex", "rb") as f:
    d = DEX(f.read())
    
    for c in d.classes:
        name = c.name
        if "Bluetooth4Profile" in name:
            print(f"\nClass: {name}")
            for fld in c.get_fields():
                print(f"  Field: {fld.name} {fld.proto}")
            for m in c.get_methods():
                print(f"  Method: {m.name} {m.proto}")
                if m.code:
                    for ins in m.code.get_instructions():
                        # check for const-string instructions
                        op = ins.get_op_name()
                        if "const-string" in op:
                            val = ins.get_string()
                            print(f"    String: {val}")

        if "Elm$AdapterType" in name:
            print(f"\nClass: {name}")
            for fld in c.get_fields():
                print(f"  Field: {fld.name}")
