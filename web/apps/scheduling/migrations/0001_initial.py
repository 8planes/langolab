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

        # Adding model 'LanguagePairUserCount'
        db.create_table('scheduling_languagepairusercount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hour', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('native_language', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
            ('foreign_language', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
            ('user_count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('scheduling', ['LanguagePairUserCount'])

        # Adding unique constraint on 'LanguagePairUserCount', fields ['hour', 'native_language', 'foreign_language']
        db.create_unique('scheduling_languagepairusercount', ['hour', 'native_language', 'foreign_language'])

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


    def backwards(self, orm):
        
        # Removing unique constraint on 'LanguagePairUserCount', fields ['hour', 'native_language', 'foreign_language']
        db.delete_unique('scheduling_languagepairusercount', ['hour', 'native_language', 'foreign_language'])

        # Deleting model 'UserScheduleRange'
        db.delete_table('scheduling_userschedulerange')

        # Deleting model 'LanguagePairUserCount'
        db.delete_table('scheduling_languagepairusercount')

        # Deleting model 'UserNotificationOptOut'
        db.delete_table('scheduling_usernotificationoptout')

        # Deleting model 'UserNotification'
        db.delete_table('scheduling_usernotification')

        # Deleting model 'UserNotificationRange'
        db.delete_table('scheduling_usernotificationrange')


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
        'scheduling.languagepairusercount': {
            'Meta': {'unique_together': "(('hour', 'native_language', 'foreign_language'),)", 'object_name': 'LanguagePairUserCount'},
            'foreign_language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'hour': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native_language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
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
