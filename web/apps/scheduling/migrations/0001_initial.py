# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserScheduleRange'
        db.create_table('scheduling_userschedulerange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['llauth.CustomUser'])),
            ('date_saved', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('scheduling', ['UserScheduleRange'])

        # Adding model 'UserNotificationOptOut'
        db.create_table('scheduling_usernotificationoptout', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['llauth.CustomUser'])),
            ('opt_out_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('scheduling', ['UserNotificationOptOut'])

        # Adding model 'UserNotification'
        db.create_table('scheduling_usernotification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['llauth.CustomUser'])),
            ('date_sent', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('date_clicked', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('scheduling', ['UserNotification'])

        # Adding model 'UserNotificationRange'
        db.create_table('scheduling_usernotificationrange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notification', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduling.UserNotification'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('scheduling', ['UserNotificationRange'])

        # Adding model 'LanguageCalendar'
        db.create_table('scheduling_languagecalendar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('native_languages', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('foreign_languages', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('scheduling', ['LanguageCalendar'])

        # Adding unique constraint on 'LanguageCalendar', fields ['native_languages', 'foreign_languages']
        db.create_unique('scheduling_languagecalendar', ['native_languages', 'foreign_languages'])

        # Adding model 'LanguageCalendarNativeLanguage'
        db.create_table('scheduling_languagecalendarnativelanguage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('calendar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduling.LanguageCalendar'])),
            ('native_language', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
        ))
        db.send_create_signal('scheduling', ['LanguageCalendarNativeLanguage'])

        # Adding unique constraint on 'LanguageCalendarNativeLanguage', fields ['calendar', 'native_language']
        db.create_unique('scheduling_languagecalendarnativelanguage', ['calendar_id', 'native_language'])

        # Adding model 'LanguageCalendarForeignLanguage'
        db.create_table('scheduling_languagecalendarforeignlanguage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('calendar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduling.LanguageCalendar'])),
            ('foreign_language', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
        ))
        db.send_create_signal('scheduling', ['LanguageCalendarForeignLanguage'])

        # Adding unique constraint on 'LanguageCalendarForeignLanguage', fields ['calendar', 'foreign_language']
        db.create_unique('scheduling_languagecalendarforeignlanguage', ['calendar_id', 'foreign_language'])

        # Adding model 'LanguageCalendarRange'
        db.create_table('scheduling_languagecalendarrange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('calendar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduling.LanguageCalendar'])),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
        ))
        db.send_create_signal('scheduling', ['LanguageCalendarRange'])

        # Adding unique constraint on 'LanguageCalendarRange', fields ['calendar', 'start_date']
        db.create_unique('scheduling_languagecalendarrange', ['calendar_id', 'start_date'])

        # Adding model 'LanguageCalendarUserCount'
        db.create_table('scheduling_languagecalendarusercount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hour', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('calendar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduling.LanguageCalendar'])),
            ('user_count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('scheduling', ['LanguageCalendarUserCount'])

        # Adding unique constraint on 'LanguageCalendarUserCount', fields ['hour', 'calendar']
        db.create_unique('scheduling_languagecalendarusercount', ['hour', 'calendar_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'LanguageCalendarUserCount', fields ['hour', 'calendar']
        db.delete_unique('scheduling_languagecalendarusercount', ['hour', 'calendar_id'])

        # Removing unique constraint on 'LanguageCalendarRange', fields ['calendar', 'start_date']
        db.delete_unique('scheduling_languagecalendarrange', ['calendar_id', 'start_date'])

        # Removing unique constraint on 'LanguageCalendarForeignLanguage', fields ['calendar', 'foreign_language']
        db.delete_unique('scheduling_languagecalendarforeignlanguage', ['calendar_id', 'foreign_language'])

        # Removing unique constraint on 'LanguageCalendarNativeLanguage', fields ['calendar', 'native_language']
        db.delete_unique('scheduling_languagecalendarnativelanguage', ['calendar_id', 'native_language'])

        # Removing unique constraint on 'LanguageCalendar', fields ['native_languages', 'foreign_languages']
        db.delete_unique('scheduling_languagecalendar', ['native_languages', 'foreign_languages'])

        # Deleting model 'UserScheduleRange'
        db.delete_table('scheduling_userschedulerange')

        # Deleting model 'UserNotificationOptOut'
        db.delete_table('scheduling_usernotificationoptout')

        # Deleting model 'UserNotification'
        db.delete_table('scheduling_usernotification')

        # Deleting model 'UserNotificationRange'
        db.delete_table('scheduling_usernotificationrange')

        # Deleting model 'LanguageCalendar'
        db.delete_table('scheduling_languagecalendar')

        # Deleting model 'LanguageCalendarNativeLanguage'
        db.delete_table('scheduling_languagecalendarnativelanguage')

        # Deleting model 'LanguageCalendarForeignLanguage'
        db.delete_table('scheduling_languagecalendarforeignlanguage')

        # Deleting model 'LanguageCalendarRange'
        db.delete_table('scheduling_languagecalendarrange')

        # Deleting model 'LanguageCalendarUserCount'
        db.delete_table('scheduling_languagecalendarusercount')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'llauth.customuser': {
            'Meta': {'object_name': 'CustomUser', '_ormbases': ['auth.User']},
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'native_language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'profile_photo_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'scheduling.languagecalendar': {
            'Meta': {'unique_together': "(('native_languages', 'foreign_languages'),)", 'object_name': 'LanguageCalendar'},
            'foreign_languages': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'native_languages': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'scheduling.languagecalendarforeignlanguage': {
            'Meta': {'unique_together': "(('calendar', 'foreign_language'),)", 'object_name': 'LanguageCalendarForeignLanguage'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduling.LanguageCalendar']"}),
            'foreign_language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'scheduling.languagecalendarnativelanguage': {
            'Meta': {'unique_together': "(('calendar', 'native_language'),)", 'object_name': 'LanguageCalendarNativeLanguage'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduling.LanguageCalendar']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native_language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'})
        },
        'scheduling.languagecalendarrange': {
            'Meta': {'unique_together': "(('calendar', 'start_date'),)", 'object_name': 'LanguageCalendarRange'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduling.LanguageCalendar']"}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'scheduling.languagecalendarusercount': {
            'Meta': {'unique_together': "(('hour', 'calendar'),)", 'object_name': 'LanguageCalendarUserCount'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduling.LanguageCalendar']"}),
            'hour': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_count': ('django.db.models.fields.IntegerField', [], {})
        },
        'scheduling.usernotification': {
            'Meta': {'object_name': 'UserNotification'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'date_clicked': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['llauth.CustomUser']"})
        },
        'scheduling.usernotificationoptout': {
            'Meta': {'object_name': 'UserNotificationOptOut'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opt_out_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['llauth.CustomUser']"})
        },
        'scheduling.usernotificationrange': {
            'Meta': {'object_name': 'UserNotificationRange'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduling.UserNotification']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'scheduling.userschedulerange': {
            'Meta': {'object_name': 'UserScheduleRange'},
            'date_saved': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['llauth.CustomUser']"})
        }
    }

    complete_apps = ['scheduling']
