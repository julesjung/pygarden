extends Area2D

@export var plant_data: PlantData

@onready var _sprite = $Sprite2D
@onready var _progress_bar = $ProgressBar

var growth_stage = 0
var start_time = Time.get_unix_time_from_system()

func _ready() -> void:
	_sprite.texture = plant_data.texture
	_sprite.hframes = 3
	_sprite.frame = 0

func _process(_delta: float) -> void:
	var elapsed = Time.get_unix_time_from_system() - start_time

	if growth_stage == 0:
		if elapsed >= plant_data.growth_time:
			growth_stage = 1
			_sprite.frame = 1
			start_time += plant_data.growth_time
			elapsed -= plant_data.growth_time
		else:
			_progress_bar.value = elapsed * 92 / plant_data.growth_time

	if growth_stage == 1:
		if elapsed >= plant_data.production_time:
			growth_stage = 2
			_sprite.frame = 2
			start_time += plant_data.production_time
			_progress_bar.hide()
		else:
			_progress_bar.value = elapsed * 92 / plant_data.production_time

func _on_input_event(_viewport: Node, event: InputEvent, _shape_idx: int) -> void:
	if event is InputEventMouseButton and event.is_pressed() and event.button_index == MOUSE_BUTTON_LEFT:
		if growth_stage == 2:
			growth_stage = 1
			_sprite.frame = 1
			start_time = Time.get_unix_time_from_system()
			_progress_bar.show()
