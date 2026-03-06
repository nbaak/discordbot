

from cogs.helldivers2.hd2_tools import convert_to_discord_italic


def test():
    tests = [
        ("test", "test"),
        ("<i=1>test123</i>", "*test123*"),
        ("<i=2>test123</i>", "**test123**"),
        ("<i=3>test123</i>", "***test123***"),
        
        ("<i=1>test123</i> and <i=2>test123</i> and <i=3>test123</i>", "*test123* and **test123** and ***test123***"),
        ("<i=1>Liberate Achernar Secundus</i> to restore the <i=1>AM Defense Factory Hub</i>, a vital asset of our most loyal contracting partner.", "*Liberate Achernar Secundus* to restore the *AM Defense Factory Hub*, a vital asset of our most loyal contracting partner.")
        ]
    
    for text, expected in tests:
        received = convert_to_discord_italic(text)
        success = expected == received
        if success:
            print(f"{received} {success}")
        else:
            print(f"'{received}' got '{expected}' {success}")


if __name__ == "__main__":
    test()
