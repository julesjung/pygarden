extends Node2D

@export var plants_data: Dictionary[String, PlantData]

var _plant_scene = preload("res://scenes/plant.tscn")

@onready var _pause_menu = $PauseMenu

var plants = []

func _ready() -> void:
	var game_data = $SaveManager.load_game()
	
	for data in game_data["plants"]:
		var plant = _plant_scene.instantiate()

		plant.position = Vector2(data["position"][0], data["position"][1])
		plant.plant_data = plants_data[data["type"]]
		plant.growth_stage = data["growth_stage"]
		plant.start_time = data["start_time"]

		add_child(plant)
		plants.append(plant)

func _input(event):
	if event is InputEventKey and event.keycode == KEY_ESCAPE:
		_pause_menu.visible = true

func _on_pause_menu_save_pressed() -> void:
	$SaveManager.save_game(plants)
