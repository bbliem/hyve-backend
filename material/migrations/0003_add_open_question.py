# Generated by Django 3.1.1 on 2021-01-30 17:08

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.blocks.static_block
import wagtail.core.fields
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0002_models'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openquestion',
            options={},
        ),
        migrations.RemoveField(
            model_name='openquestion',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='openquestion',
            name='sort_order',
        ),
        migrations.AlterField(
            model_name='lessonpage',
            name='body',
            field=wagtail.core.fields.StreamField([('lesson_content', wagtail.core.blocks.RichTextBlock()), ('page_break', wagtail.core.blocks.static_block.StaticBlock()), ('quiz', wagtail.snippets.blocks.SnippetChooserBlock('material.Quiz')), ('open_question', wagtail.snippets.blocks.SnippetChooserBlock('material.OpenQuestion'))], blank=True),
        ),
    ]
