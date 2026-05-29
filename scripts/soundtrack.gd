extends Node

@export var tracks: Array[AudioStream]
var _current_index: int = 0

var _player: AudioStreamPlayer

func _ready() -> void:
	_player = AudioStreamPlayer.new()
	add_child(self._player)
	
	tracks.shuffle()
	_play()
	
	_player.finished.connect(_finished)

func _play() -> void:
	_player.stream = tracks[_current_index]
	_player.play()

func _finished() -> void:
	_current_index = (_current_index + 1) % len(tracks)
	_play()
