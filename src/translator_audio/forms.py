from django import forms

class AudioUploadForm(forms.Form):
    audio_file = forms.FileField(label="Selecione o arquivo de áudio")

class AudioRecordForm(forms.Form):
    recorded_audio = forms.CharField(widget=forms.HiddenInput(), required=False)
