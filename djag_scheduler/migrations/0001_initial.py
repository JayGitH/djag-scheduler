# Generated by Django 3.1.2 on 2021-10-22 16:53

import djag_scheduler.models.crontab_schedule_model
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrontabSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minute', models.CharField(default='*', help_text='Cron Minutes to Run. Use "*" for "all". (Example: "0,30")', max_length=240, verbose_name='Minute(s)')),
                ('hour', models.CharField(default='*', help_text='Cron Hours to Run. Use "*" for "all". (Example: "8,20")', max_length=96, verbose_name='Hour(s)')),
                ('day_of_week', models.CharField(default='*', help_text='Cron Days Of The Week to Run. Use "*" for "all". (Example: "0,5")', max_length=64, verbose_name='Day(s) Of The Week')),
                ('day_of_month', models.CharField(default='*', help_text='Cron Days Of The Month to Run. Use "*" for "all". (Example: "1,15")', max_length=124, verbose_name='Day(s) Of The Month')),
                ('month_of_year', models.CharField(default='*', help_text='Cron Months Of The Year to Run. Use "*" for "all". (Example: "0,6")', max_length=64, verbose_name='Month(s) Of The Year')),
                ('timezone', timezone_field.fields.TimeZoneField(default=djag_scheduler.models.crontab_schedule_model.default_timezone, help_text='Timezone to Run the Cron Schedule on. Default is UTC.', verbose_name='Cron Timezone')),
            ],
            options={
                'verbose_name': 'crontab',
                'verbose_name_plural': 'crontabs',
                'ordering': ['month_of_year', 'day_of_month', 'day_of_week', 'hour', 'minute', 'timezone'],
            },
        ),
        migrations.CreateModel(
            name='PeriodicTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Short Description For This Task', max_length=200, unique=True, verbose_name='Name')),
                ('task', models.CharField(help_text='The Name of the Celery Task that Should be Run.  (Example: "proj.tasks.import_contacts")', max_length=200, unique=True, verbose_name='Task Name')),
                ('cron_base', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='Cron base from which tasks are run (defaults to create time if blank)', verbose_name='Cron Base')),
                ('args', models.JSONField(blank=True, default=list, help_text='JSON encoded positional arguments (Example: ["arg1", "arg2"])', verbose_name='Positional Arguments')),
                ('kwargs', models.JSONField(blank=True, default=dict, help_text='JSON encoded keyword arguments (Example: {"argument": "value"})', verbose_name='Keyword Arguments')),
                ('queue', models.CharField(blank=True, default=None, help_text='Queue defined in CELERY_TASK_QUEUES. Leave None for default queuing.', max_length=200, null=True, verbose_name='Queue Override')),
                ('exchange', models.CharField(blank=True, default=None, help_text='Override Exchange for low-level AMQP routing', max_length=200, null=True, verbose_name='Exchange')),
                ('routing_key', models.CharField(blank=True, default=None, help_text='Override Routing Key for low-level AMQP routing', max_length=200, null=True, verbose_name='Routing Key')),
                ('headers', models.JSONField(blank=True, default=dict, help_text='JSON encoded message headers for the AMQP message.', verbose_name='AMQP Message Headers')),
                ('priority', models.PositiveIntegerField(blank=True, default=None, help_text='Priority Number between 0 and 255. Supported by: RabbitMQ, Redis (priority reversed, 0 is highest).', null=True, validators=[django.core.validators.MaxValueValidator(255)], verbose_name='Priority')),
                ('enabled', models.BooleanField(default=True, help_text='Set to False to disable the schedule', verbose_name='Enable Task')),
                ('skip_misfire', models.BooleanField(default=False, help_text='Skip all misfire events', verbose_name='Skip Misfires')),
                ('coalesce_misfire', models.BooleanField(default=False, help_text='Coalesce all misfire events into one event', verbose_name='Coalesce Misfires')),
                ('grace_period', models.PositiveIntegerField(blank=True, default=None, help_text='Misfire grace period in seconds', null=True, verbose_name='Grace Period')),
                ('last_cron', models.DateTimeField(blank=True, editable=False, help_text='The last cron djag-scheduler completed running', null=True, verbose_name='Last Ran Cron')),
                ('last_cron_start', models.DateTimeField(blank=True, default=None, editable=False, help_text="Task's last cron start time", null=True, verbose_name='Last Cron Start Time')),
                ('last_cron_end', models.DateTimeField(blank=True, default=None, editable=False, help_text="Task's last cron end time", null=True, verbose_name='Last Cron End Time')),
                ('running', models.IntegerField(default=0, editable=False, help_text='Total running instances of the task at the moment', verbose_name='Running Instances')),
                ('total_run_count', models.PositiveIntegerField(default=0, editable=False, help_text='Running count of how many times the schedule has triggered the task', verbose_name='Total Run Count')),
                ('date_changed', models.DateTimeField(auto_now=True, help_text='Datetime that this PeriodicTask was last modified', verbose_name='Last Modified')),
                ('description', models.TextField(blank=True, help_text='Detailed description about the details of this Periodic Task', verbose_name='Description')),
                ('crontab', models.ForeignKey(help_text='Crontab Schedule to run the task on.', on_delete=django.db.models.deletion.CASCADE, to='djag_scheduler.crontabschedule', verbose_name='Crontab Schedule')),
            ],
            options={
                'verbose_name': 'periodic task',
                'verbose_name_plural': 'periodic tasks',
            },
        ),
        migrations.CreateModel(
            name='UserAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.IntegerField(choices=[(-1, 'Task Changed'), (-2, 'Schedule Changed'), (-3, 'Dependency Changed'), (1, 'Unclassified Action')], help_text='Action to be performed', verbose_name='User Action')),
                ('payload', models.JSONField(default=dict, help_text="Action's payload data", verbose_name='Action Payload')),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='Creation DateTime')),
            ],
            options={
                'verbose_name': 'User Action',
                'verbose_name_plural': 'User Actions',
            },
        ),
        migrations.CreateModel(
            name='UserActionAudit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.IntegerField(choices=[(-1, 'Task Changed'), (-2, 'Schedule Changed'), (-3, 'Dependency Changed'), (1, 'Unclassified Action')], help_text='Action to be performed', verbose_name='User Action')),
                ('payload', models.JSONField(default=dict, help_text="Action's payload data", verbose_name='Action Payload')),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='Creation DateTime')),
                ('delete_dt', models.DateTimeField(auto_now_add=True, verbose_name='Deletion DateTime')),
            ],
            options={
                'verbose_name': 'User Action Audit',
                'verbose_name_plural': 'User Action Audits',
            },
        ),
        migrations.CreateModel(
            name='TaskDependency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('future_depends', models.BooleanField(default=False, help_text='Depender is Future Dependent on Dependee', verbose_name='Future Dependency')),
                ('change_dt', models.DateTimeField(auto_now=True, help_text='Date Time at which dependency is created/changed', verbose_name='Change Date')),
                ('dependee', models.ForeignKey(help_text='Task Dependent by Depender', on_delete=django.db.models.deletion.CASCADE, related_name='dependee_task', to='djag_scheduler.periodictask', verbose_name='Dependee')),
                ('depender', models.ForeignKey(help_text='Task Dependent on Dependee', on_delete=django.db.models.deletion.CASCADE, related_name='depender_task', to='djag_scheduler.periodictask', verbose_name='Depender')),
            ],
            options={
                'verbose_name': 'Task Dependency',
                'verbose_name_plural': 'Task Dependencies',
            },
        ),
        migrations.AddConstraint(
            model_name='taskdependency',
            constraint=models.UniqueConstraint(fields=('depender', 'dependee'), name='task_set'),
        ),
    ]