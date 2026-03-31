extends Node2D

var _shop_ui = preload("res://scenes/shop_ui.tscn").instantiate()

func _on_shop_input_event(_viewport: Node, event: InputEvent, _shape_idx: int) -> void:
	if event is InputEventMouseButton and event.is_pressed() and event.button_index == MOUSE_BUTTON_LEFT:
		add_child(_shop_ui)
