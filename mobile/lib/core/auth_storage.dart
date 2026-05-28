import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

final sharedPrefsProvider = Provider<SharedPreferences>(
  (_) => throw UnimplementedError('Override in ProviderScope'),
);

const _tokenKey = 'farmbrain.token';
const _apiUrlKey = 'farmbrain.api_url';
const _defaultApiUrl = 'http://10.0.2.2:8000/api/v1';

class AuthStorage {
  AuthStorage(this._prefs);
  final SharedPreferences _prefs;

  String? get token => _prefs.getString(_tokenKey);
  Future<void> setToken(String? value) async {
    if (value == null) {
      await _prefs.remove(_tokenKey);
    } else {
      await _prefs.setString(_tokenKey, value);
    }
  }

  String get apiUrl => _prefs.getString(_apiUrlKey) ?? _defaultApiUrl;
  Future<void> setApiUrl(String value) => _prefs.setString(_apiUrlKey, value);
}

final authStorageProvider = Provider<AuthStorage>(
  (ref) => AuthStorage(ref.watch(sharedPrefsProvider)),
);
