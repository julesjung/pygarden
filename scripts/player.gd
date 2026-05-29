extends Node2D

func _process(delta: float) -> void:
	var input_direction = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	var new_position = global_position + input_direction * 256 * delta
	global_position.x = clamp(new_position.x, -512, 512)
	global_position.y = clamp(new_position.y, -384, 384)
