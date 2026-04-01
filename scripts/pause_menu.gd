extends CanvasLayer

signal save_pressed

func _ready() -> void:
	visible = false

func _on_continue_button_pressed() -> void:
	visible = false

func _on_save_button_pressed() -> void:
	emit_signal("save_pressed")
