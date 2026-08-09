from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from django_summernote.widgets import SummernoteWidget
import json

from apps.file_uploader.upload_utils import upload_file_to_digital_ocean, delete_file_from_digital_ocean
from .models import MultimediaAsset, NewsArticle, Content


# -----------------------------------------------
# Cache clear — signal
# -----------------------------------------------
def clear_multimedia_cache(sender, instance, **kwargs):
    cache.delete(f"multimedia_detail_{instance.pk}")
    cache.delete("multimedia_list")

def clear_article_cache(sender, instance, **kwargs):
    cache.delete("article_list")

def clear_content_cache(sender, instance, **kwargs):
    cache.delete("content_list")

post_save.connect(clear_multimedia_cache, sender=MultimediaAsset)
post_delete.connect(clear_multimedia_cache, sender=MultimediaAsset)
post_save.connect(clear_article_cache, sender=NewsArticle)
post_delete.connect(clear_article_cache, sender=NewsArticle)
post_save.connect(clear_content_cache, sender=Content)
post_delete.connect(clear_content_cache, sender=Content)


# -----------------------------------------------
# Summernote Media Button JS
# -----------------------------------------------
def get_media_button_js():
    multimedia_list = list(MultimediaAsset.objects.values("id", "title", "content_type"))
    return mark_safe(f"""
    <script>
    (function($) {{
        if (!$.summernote) return;
        $.summernote.plugins['insertMedia'] = function(context) {{
            var self = this;
            var ui = $.summernote.ui;
            var multimedia = {json.dumps(multimedia_list)};

            this.initialize = function() {{}};

            this.events = {{
                'summernote.init': function() {{}}
            }};
        }};
    }})(jQuery);
    </script>
    """)


def summernote_widget_with_media():
    multimedia_list = list(MultimediaAsset.objects.values("id", "title", "content_type"))
    media_options = "".join([
        f'<option value="{m["id"]}">[{m["content_type"]}] {m["title"] or "Untitled"}</option>'
        for m in multimedia_list
    ])

    extra_js = mark_safe(f"""
    <script>
    document.addEventListener("DOMContentLoaded", function() {{
        function initMediaButton() {{
            var editors = document.querySelectorAll(".note-toolbar");
            editors.forEach(function(toolbar) {{
                if (toolbar.querySelector(".media-insert-btn")) return;

                var wrap = document.createElement("div");
                wrap.className = "note-btn-group btn-group";
                wrap.style.cssText = "display:inline-flex;align-items:center;gap:4px;margin-left:4px;";

                var select = document.createElement("select");
                select.innerHTML = '<option value="">-- Select Media --</option>' + '{media_options}';
                select.style.cssText = "padding:4px 6px;font-size:12px;border:1px solid #ccc;border-radius:4px;height:30px;";

                var btn = document.createElement("button");
                btn.type = "button";
                btn.className = "media-insert-btn note-btn btn btn-default btn-sm";
                btn.innerHTML = "🎬 Insert";
                btn.style.cssText = "background:#3b2db5;color:#fff;border:none;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:12px;height:30px;";

                btn.addEventListener("click", function() {{
                    var id = select.value;
                    if (!id) {{ alert("Please select a media item"); return; }}
                    var text = select.options[select.selectedIndex].text;
                    var tag = '<span class="media-embed" data-media-id="' + id + '" contenteditable="false" style="display:inline-block;padding:3px 10px;background:#e8e4ff;color:#3b2db5;border-radius:4px;cursor:pointer;font-size:13px;user-select:none;">🎬 ' + text + '</span>&nbsp;';

                    var editable = toolbar.closest(".note-editor").querySelector(".note-editable");
                    if (editable) {{
                        editable.focus();
                        document.execCommand("insertHTML", false, tag);
                    }}
                    select.value = "";
                }});

                wrap.appendChild(select);
                wrap.appendChild(btn);
                toolbar.appendChild(wrap);
            }});
        }}

        // Retry until summernote toolbar renders
        var attempts = 0;
        var interval = setInterval(function() {{
            var toolbars = document.querySelectorAll(".note-toolbar");
            if (toolbars.length > 0) {{
                initMediaButton();
                clearInterval(interval);
            }}
            if (++attempts > 20) clearInterval(interval);
        }}, 300);
    }});
    </script>
    """)

    return extra_js


# -----------------------------------------------
# MultimediaAsset
# -----------------------------------------------
class MultimediaAssetForm(forms.ModelForm):
    upload_file  = forms.FileField(required=False, label="File Upload (Image / Audio / Video)")
    youtube_url  = forms.URLField(required=False, label="YouTube URL")
    text_content = forms.CharField(
        required=False,
        label="Text Content",
        widget=forms.Textarea(attrs={"rows": 4, "disabled": True, "id": "id_text_content"})
    )

    class Meta:
        model = MultimediaAsset
        fields = ["title", "content_type", "upload_file", "youtube_url", "text_content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["upload_file"].widget.attrs.update({"disabled": True, "id": "id_upload_file"})
        self.fields["youtube_url"].widget.attrs.update({"disabled": True, "id": "id_youtube_url"})
        self.fields["content_type"].widget.attrs.update({"onchange": "handleTypeChange(this.value)"})

        if self.instance.pk and self.instance.file:
            file_url = self.instance.file
            content_type = self.instance.content_type

            if content_type == "image":
                self.fields["upload_file"].help_text = mark_safe(f'<div style="margin-top:10px;"><img src="{file_url}" style="max-height:150px;border-radius:8px;border:1px solid #e5e7eb;"></div>')
            elif content_type == "audio":
                self.fields["upload_file"].help_text = mark_safe(f'<div style="margin-top:10px;"><audio controls style="width:100%;"><source src="{file_url}"></audio></div>')
            elif content_type == "video":
                self.fields["upload_file"].help_text = mark_safe(f'<div style="margin-top:10px;"><video controls style="max-width:100%;border-radius:8px;"><source src="{file_url}"></video></div>')
            elif content_type == "youtube":
                self.fields["youtube_url"].initial = file_url
                self.fields["youtube_url"].help_text = mark_safe(f'<div style="margin-top:10px;"><a href="{file_url}" target="_blank">{file_url}</a></div>')
            elif content_type == "text":
                self.fields["text_content"].initial = file_url

        self.fields["content_type"].help_text = mark_safe("""
        <script>
        document.addEventListener("DOMContentLoaded", function() {
            const contentType = document.getElementById("id_content_type");
            if (contentType) handleTypeChange(contentType.value);
        });
        function handleTypeChange(type) {
            const upload  = document.getElementById("id_upload_file");
            const youtube = document.getElementById("id_youtube_url");
            const text    = document.getElementById("id_text_content");
            [upload, youtube, text].forEach(el => { if (el) el.disabled = true; });
            if (["image", "audio", "video"].includes(type) && upload) upload.disabled = false;
            else if (type === "youtube" && youtube) youtube.disabled = false;
            else if (type === "text" && text) text.disabled = false;
        }
        </script>
        """)

    def save(self, commit=True):
        instance = super().save(commit=False)
        content_type = self.cleaned_data.get("content_type")

        if content_type in ["image", "audio", "video"]:
            file = self.cleaned_data.get("upload_file")
            if file:
                if instance.file:
                    try:
                        delete_file_from_digital_ocean(instance.file)
                    except Exception:
                        pass
                instance.file = upload_file_to_digital_ocean(file, folder="multimedia")
        elif content_type == "youtube":
            youtube_url = self.cleaned_data.get("youtube_url")
            if youtube_url:
                instance.file = youtube_url
        elif content_type == "text":
            text_content = self.cleaned_data.get("text_content")
            if text_content:
                instance.file = text_content

        if commit:
            instance.save()
        return instance


@admin.register(MultimediaAsset)
class MultimediaAssetAdmin(admin.ModelAdmin):
    form = MultimediaAssetForm
    list_display = ["title", "id", "content_type", "created_at"]
    list_filter = ["content_type"]


# -----------------------------------------------
# NewsArticle
# -----------------------------------------------
class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = "__all__"
        widgets = {
            "body": SummernoteWidget()
        }


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    form = NewsArticleForm
    list_display = ["title", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["title"]


# -----------------------------------------------
# Content
# -----------------------------------------------
class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = "__all__"
        widgets = {
            "body": SummernoteWidget()
        }


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    form = ContentForm
    list_display = ["title", "created_at"]
    search_fields = ["title"]