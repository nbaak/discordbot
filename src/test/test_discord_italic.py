
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from cogs.helldivers2.hd2_tools import convert_to_discord_italic


def test():
    tests = [
        ("test", "test"),
        ("<i=1>test123</i>", "*test123*"),
        ("<i=1>test123</i> <i=1>test567</i>", "*test123* *test567*"),
        ("<i=2>test123</i>", "**test123**"),
        ("<i=3>test123</i>", "***test123***"),
        
        ("<i=1>test123</i> and <i=2>test123</i> and <i=3>test123</i>", "*test123* and **test123** and ***test123***"),
        ("<i=1>Liberate Achernar Secundus</i> to restore the <i=1>AM Defense Factory Hub</i>, a vital asset of our most loyal contracting partner.", "*Liberate Achernar Secundus* to restore the *AM Defense Factory Hub*, a vital asset of our most loyal contracting partner.")
        ]
    
    successful = failed = 0
    
    for text, expected in tests:
        received = convert_to_discord_italic(text)
        success = expected == received
        if success:
            print(f"{received} {success}")
            successful += 1
        else:
            print(f"'{received}' got '{expected}' {success}")
            failed += 1
    
    print(f"successful: {successful}/{len(tests)}")
    print(f"failed    : {failed}/{len(tests)}")


if __name__ == "__main__":
    test()
