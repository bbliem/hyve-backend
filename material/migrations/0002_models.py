# Generated by Django 3.1.1 on 2021-02-21 16:18

from django.db import migrations, models
import django.db.models.deletion
import material.blocks
import modelcluster.fields
import uuid
import wagtail.core.blocks
import wagtail.core.blocks.static_block
import wagtail.core.fields
import wagtailvideos.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0060_fix_workflow_unique_constraint'),
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('description', wagtail.core.fields.RichTextField(blank=True)),
                ('description_en', wagtail.core.fields.RichTextField(blank=True, null=True)),
                ('description_fi', wagtail.core.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('description', wagtail.core.fields.RichTextField(blank=True)),
                ('description_en', wagtail.core.fields.RichTextField(blank=True, null=True)),
                ('description_fi', wagtail.core.fields.RichTextField(blank=True, null=True)),
                ('body', wagtail.core.fields.StreamField([('lesson_content', wagtail.core.blocks.RichTextBlock()), ('video', wagtailvideos.blocks.VideoChooserBlock()), ('page_break', wagtail.core.blocks.static_block.StaticBlock()), ('quiz', material.blocks.QuizBlock()), ('open_question', wagtail.core.blocks.RichTextBlock())], blank=True)),
                ('body_en', wagtail.core.fields.StreamField([('lesson_content', wagtail.core.blocks.RichTextBlock()), ('video', wagtailvideos.blocks.VideoChooserBlock()), ('page_break', wagtail.core.blocks.static_block.StaticBlock()), ('quiz', material.blocks.QuizBlock()), ('open_question', wagtail.core.blocks.RichTextBlock())], blank=True, null=True)),
                ('body_fi', wagtail.core.fields.StreamField([('lesson_content', wagtail.core.blocks.RichTextBlock()), ('video', wagtailvideos.blocks.VideoChooserBlock()), ('page_break', wagtail.core.blocks.static_block.StaticBlock()), ('quiz', material.blocks.QuizBlock()), ('open_question', wagtail.core.blocks.RichTextBlock())], blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='OpenQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('internal_name', models.CharField(max_length=250, unique=True)),
                ('text', models.CharField(blank=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('internal_name', models.CharField(max_length=250, unique=True)),
            ],
            options={
                'verbose_name_plural': 'quizzes',
            },
        ),
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
                ('body_en', wagtail.core.fields.RichTextField(blank=True, null=True)),
                ('body_fi', wagtail.core.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.CharField(blank=True, max_length=250)),
                ('quiz', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='material.quiz')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MultipleChoiceAnswer',
            fields=[
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.CharField(blank=True, max_length=250)),
                ('correct', models.BooleanField(default=False)),
                ('explanation', models.CharField(blank=True, max_length=250)),
                ('question', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='material.multiplechoicequestion')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='organization',
            name='lessons',
            field=models.ManyToManyField(blank=True, to='material.Lesson'),
        ),
    ]
