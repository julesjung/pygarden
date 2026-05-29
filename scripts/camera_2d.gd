extends Camera2D

var is_panning := false
var last_mouse_position = Vector2.ZERO
var zoom_x = 1
var zoom_y = 1

func _input(event):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_RIGHT:
			is_panning = event.is_pressed()
			last_mouse_position = get_global_mouse_position()

		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			if zoom.x < 2 && zoom.y < 2:
				var mouse_position = get_global_mouse_position()
				var pre_zoom_value = zoom
				zoom_x += 0.25
				zoom_y += 0.25
				zoom = Vector2(zoom_x, zoom_y)
				position += (mouse_position - global_position) * (Vector2(1, 1) - pre_zoom_value / zoom)

		if event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			if zoom.x > 1 && zoom.y > 1:
				var mouse_position = get_global_mouse_position()
				var pre_zoom_value = zoom
				zoom_x -= 0.25
				zoom_y -= 0.25
				zoom = Vector2(zoom_x, zoom_y)
				position += (mouse_position - global_position) * (Vector2(1, 1) - pre_zoom_value / zoom)
				

	if event is InputEventMouseMotion and is_panning:
		var current = get_global_mouse_position()
		offset += last_mouse_position - current
