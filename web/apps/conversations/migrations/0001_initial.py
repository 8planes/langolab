"""
Langolab -- learn foreign languages by speaking with random native speakers over webcam.
Copyright (C) 2011 Adam Duston

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Conversation'
        db.create_table('conversations_conversation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_started', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('language_0', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('language_1', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('user_0', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_0', to=orm['llauth.CustomUser'])),
            ('user_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_1', to=orm['llauth.CustomUser'])),
            ('near_id_0', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('near_id_1', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('conversations', ['Conversation'])

        # Adding model 'WaitingUser'
        db.create_table('conversations_waitinguser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['llauth.CustomUser'])),
            ('time_started', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_ping', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('conversation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conversations.Conversation'], null=True)),
            ('near_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('conversations', ['WaitingUser'])

        # Adding model 'WaitingUserLanguagePair'
        db.create_table('conversations_waitinguserlanguagepair', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('waiting_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conversations.WaitingUser'])),
            ('native_language', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('foreign_language', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('last_ping', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('conversations', ['WaitingUserLanguagePair'])

        # Adding model 'WaitingConversation'
        db.create_table('conversations_waitingconversation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('waiting_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conversations.WaitingUser'])),
            ('native_language', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
            ('foreign_language', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
        ))
        db.send_create_signal('conversations', ['WaitingConversation'])

        # Adding model 'CompletedWait'
        db.create_table('conversations_completedwait', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['llauth.CustomUser'])),
            ('time_started', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_ping', self.gf('django.db.models.fields.DateTimeField')()),
            ('native_language', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
            ('matched_foreign_language', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
            ('foreign_languages', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('resulting_conversation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conversations.Conversation'])),
        ))
        db.send_create_signal('conversations', ['CompletedWait'])

        # Adding model 'AbandonedWait'
        db.create_table('conversations_abandonedwait', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['llauth.CustomUser'])),
            ('time_started', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_ping', self.gf('django.db.models.fields.DateTimeField')()),
            ('native_language', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
            ('foreign_languages', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('conversations', ['AbandonedWait'])


    def backwards(self, orm):
        
        # Deleting model 'Conversation'
        db.delete_table('conversations_conversation')

        # Deleting model 'WaitingUser'
        db.delete_table('conversations_waitinguser')

        # Deleting model 'WaitingUserLanguagePair'
        db.delete_table('conversations_waitinguserlanguagepair')

        # Deleting model 'WaitingConversation'
        db.delete_table('conversations_waitingconversation')

        # Deleting model 'CompletedWait'
        db.delete_table('conversations_completedwait')

        # Deleting model 'AbandonedWait'
        db.delete_table('conversations_abandonedwait')


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
        'conversations.abandonedwait': {
            'Meta': {'object_name': 'AbandonedWait'},
            'foreign_languages': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_ping': ('django.db.models.fields.DateTimeField', [], {}),
            'native_language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'time_started': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['llauth.CustomUser']"})
        },
        'conversations.completedwait': {
            'Meta': {'object_name': 'CompletedWait'},
            'foreign_languages': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_ping': ('django.db.models.fields.DateTimeField', [], {}),
            'matched_foreign_language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'native_language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'resulting_conversation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conversations.Conversation']"}),
            'time_started': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['llauth.CustomUser']"})
        },
        'conversations.conversation': {
            'Meta': {'object_name': 'Conversation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_0': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'language_1': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'near_id_0': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'near_id_1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time_started': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user_0': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_0'", 'to': "orm['llauth.CustomUser']"}),
            'user_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_1'", 'to': "orm['llauth.CustomUser']"})
        },
        'conversations.waitingconversation': {
            'Meta': {'object_name': 'WaitingConversation'},
            'foreign_language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native_language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'waiting_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conversations.WaitingUser']"})
        },
        'conversations.waitinguser': {
            'Meta': {'object_name': 'WaitingUser'},
            'conversation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conversations.Conversation']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_ping': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'near_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time_started': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['llauth.CustomUser']"})
        },
        'conversations.waitinguserlanguagepair': {
            'Meta': {'object_name': 'WaitingUserLanguagePair'},
            'foreign_language': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_ping': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'native_language': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'waiting_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conversations.WaitingUser']"})
        },
        'llauth.customuser': {
            'Meta': {'object_name': 'CustomUser', '_ormbases': ['auth.User']},
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'native_language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'profile_photo_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['conversations']
