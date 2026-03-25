"""
ground types:
0 = plains (top-left)
1 = aquatic (bottom-left)
2 = tropical (bottom-right)

prices/yields in leaves

times in seconds
"""

oak = {
    "name": "Chêne",
    "spritesheet": "assets/plants/tree.png",
    "price": 100,
    "yield": 100,
    "time_to_grow_adult": 5,
    "time_to_grow_leaves": 60,
    "ground_type": 0,
}

sakura = {
    "name": "Cerisier du Japon",
    "spritesheet": "assets/plants/sakura.png",
    "price": 300,
    "yield": 500,
    "time_to_grow_adult": 60,
    "time_to_grow_leaves": 120,
    "ground_type": 0,
}

birch = {
    "name": "Bouleau",
    "spritesheet": "assets/plants/birch_tree.png",
    "price": 3000,
    "yield": 4500,
    "time_to_grow_adult": 900,
    "time_to_grow_leaves": 1800,
    "ground_type": 0,
}

pine = {
    "name": "Sapin",
    "spritesheet": "assets/plants/pine_tree.png",
    "price": 10000,
    "yield": 10000,
    "time_to_grow_adult": 3600,
    "time_to_grow_leaves": 3600,
    "ground_type": 0,
}

clovers = {
    "name": "Trèfles",
    "spritesheet": "assets/plants/clover.png",
    "price": 50000,
    "yield": 35000,
    "time_to_grow_adult": 7200,
    "time_to_grow_leaves": 5400,
    "ground_type": 1,
}

kelp = {
    "name": "Algues",
    "spritesheet": "assets/plants/kelp.png",
    "price": 200000,
    "yield": 150000,
    "time_to_grow_adult": 21600,
    "time_to_grow_leaves": 7200,
    "ground_type": 1,
}

nenuphar = {
    "name": "Nénuphar",
    "spritesheet": "assets/plants/nenuphar.png",
    "price": 500000,
    "yield": 300000,
    "time_to_grow_adult": 43200,
    "time_to_grow_leaves": 7200,
    "ground_type": 1,
}

corals = {
    "name": "Coraux",
    "spritesheet": "assets/plants/corals.png",
    "price": 1250000,
    "yield": 1000000,
    "time_to_grow_adult": 86400,
    "time_to_grow_leaves": 10800,
    "ground_type": 1,
}

acacia = {
    "name": "Acacia",
    "spritesheet": "assets/plants/acacia.png",
    "price": 5000000,
    "yield": 3000000,
    "time_to_grow_adult": 172800,
    "time_to_grow_leaves": 14400,
    "ground_type": 2,
}

cactus = {
    "name": "Cactus",
    "spritesheet": "assets/plants/cactus.png",
    "price": 20000000,
    "yield": 15000000,
    "time_to_grow_adult": 259200,
    "time_to_grow_leaves": 21600,
    "ground_type": 2,
}

palm = {
    "name": "Palmier",
    "spritesheet": "assets/plants/palm.png",
    "price": 100000000,
    "yield": 60000000,
    "time_to_grow_adult": 432000,
    "time_to_grow_leaves": 21600,
    "ground_type": 2,
}

jungle = {
    "name": "Baobab",
    "spritesheet": "assets/plants/jungle.png",
    "price": 1000000000,
    "yield": 100000000,
    "time_to_grow_adult": 604800,
    "time_to_grow_leaves": 25200,
    "ground_type": 2,
}


plants = [
    oak,
    sakura,
    birch,
    pine,
    clovers,
    kelp,
    nenuphar,
    corals,
    acacia,
    cactus,
    palm,
    jungle,
]
