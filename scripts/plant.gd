extends Area2D

@export var plant_data: PlantData
@onready var _sprite = $Sprite2D

var growth_stage = 0
var start_time = Time.get_unix_time_from_system()

func _ready() -> void:
	_sprite.texture = plant_data.texture
	_sprite.hframes = 3
	_sprite.frame = 0

func _process(_delta: float) -> void:
	var elapsed = Time.get_unix_time_from_system() - start_time
	
	if growth_stage == 0 and elapsed >= plant_data.growth_time:
		growth_stage = 1
		_sprite.frame = 1
		start_time += plant_data.growth_time
		elapsed -= plant_data.growth_time
	
	if growth_stage == 1 and elapsed >= plant_data.production_time:
		growth_stage = 2
		_sprite.frame = 2
		start_time += plant_data.production_time

func _on_input_event(viewport: Node, event: InputEvent, shape_idx: int) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if growth_stage == 2:
			growth_stage = 1
			_sprite.frame = 1
			start_time = Time.get_unix_time_from_system()
