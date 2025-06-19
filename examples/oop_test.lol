HAI 1.2

BTW -- CONDITIONAL STATEMENTS TEST --

I HAS A temperature ITZ 25
VISIBLE "Temperature is:"
VISIBLE temperature

BOTH SAEM temperature AN 25
O RLY?
    YA RLY
        VISIBLE "It's a nice day!"
OIC

DIFFRINT temperature AN 20
O RLY?
    YA RLY
        VISIBLE "Temperature is not 20."
OIC

I HAS A accessAllowed ITZ FAIL

accessAllowed
O RLY?
    YA RLY
        VISIBLE "This should not be printed."
    NO WAI
        VISIBLE "Access denied, as expected."
OIC

VISIBLE "---"

BTW -- BUKKIT (ARRAY) TEST --

I HAS A myBukkit ITZ A BUKKIT
VISIBLE "Created an empty bukkit:"
VISIBLE myBukkit

BTW Assigning values
myBukkit'Z ITZ 0 R "First item"
myBukkit'Z ITZ 1 R 123
myBukkit'Z ITZ 3 R WIN

VISIBLE "Bukkit after assignment:"
VISIBLE myBukkit

VISIBLE "Accessing items:"
VISIBLE "Item 0:"
VISIBLE myBukkit'Z ITZ 0
VISIBLE "Item 1:"
VISIBLE myBukkit'Z ITZ 1
VISIBLE "Item 2 (should be NOOB):"
VISIBLE myBukkit'Z ITZ 2
VISIBLE "Item 3:"
VISIBLE myBukkit'Z ITZ 3

I HAS A bukkitSize ITZ MAEK myBukkit A NUMBR
VISIBLE "Size of bukkit is:"
VISIBLE bukkitSize

BOTH SAEM bukkitSize AN 4
O RLY?
    YA RLY
        VISIBLE "Size check passed!"
    NO WAI
        VISIBLE "Size check failed!"
OIC

KTHXBYE