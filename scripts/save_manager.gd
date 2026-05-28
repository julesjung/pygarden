extends Node

const SAVE_PATH = "user://game_data.bin"
const DEFAULT_DATA = {
	"leaves": 100,
	"plants": []
}

func load_game() -> Dictionary:
	if not FileAccess.file_exists(SAVE_PATH):
		return DEFAULT_DATA

	var file = FileAccess.open(SAVE_PATH, FileAccess.READ)
	var data = file.get_buffer(file.get_length())
	return bytes_to_var(data)

func save_game(plants: Array):
	var plants_data = []
	for plant in plants:
		plants_data.append(plant.save())
	var data = var_to_bytes({
		"leaves": 100,
		"plants": plants_data
	})
	
	var file = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	file.store_buffer(data)
