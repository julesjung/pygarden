extends Node2D

func _process(delta: float) -> void:
	var input_direction = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	global_position += input_direction * 256 * delta
