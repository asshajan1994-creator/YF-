import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api_client.dart';
import '../../core/auth_storage.dart';

class AuthState {
  const AuthState({this.user, this.loading = false, this.error});
  final Map<String, dynamic>? user;
  final bool loading;
  final String? error;

  bool get isAuthenticated => user != null;

  AuthState copyWith({Map<String, dynamic>? user, bool? loading, String? error, bool clearUser = false}) {
    return AuthState(
      user: clearUser ? null : user ?? this.user,
      loading: loading ?? this.loading,
      error: error,
    );
  }
}

class AuthController extends StateNotifier<AuthState> {
  AuthController(this._api, this._storage) : super(const AuthState(loading: true)) {
    _bootstrap();
  }

  final ApiClient _api;
  final AuthStorage _storage;

  Future<void> _bootstrap() async {
    if (_storage.token == null) {
      state = const AuthState();
      return;
    }
    try {
      final me = await _api.me();
      state = AuthState(user: me);
    } catch (_) {
      await _storage.setToken(null);
      state = const AuthState();
    }
  }

  Future<void> login(String email, String password) async {
    state = state.copyWith(loading: true, error: null);
    try {
      final data = await _api.login(email, password);
      await _storage.setToken(data['access_token'] as String);
      final me = await _api.me();
      state = AuthState(user: me);
    } catch (e) {
      state = state.copyWith(loading: false, error: _humanize(e));
    }
  }

  Future<void> register({
    required String fullName,
    required String email,
    required String password,
    String? phone,
  }) async {
    state = state.copyWith(loading: true, error: null);
    try {
      await _api.register({
        'full_name': fullName,
        'email': email,
        'password': password,
        if (phone != null && phone.isNotEmpty) 'phone': phone,
      });
      await login(email, password);
    } catch (e) {
      state = state.copyWith(loading: false, error: _humanize(e));
    }
  }

  Future<void> logout() async {
    await _storage.setToken(null);
    state = const AuthState();
  }

  String _humanize(Object e) {
    final msg = e.toString();
    if (msg.contains('401')) return 'Invalid email or password';
    if (msg.contains('SocketException') || msg.contains('Connection')) {
      return 'Cannot reach the server. Check the API URL.';
    }
    return msg;
  }
}

final authProvider = StateNotifierProvider<AuthController, AuthState>(
  (ref) => AuthController(ref.watch(apiClientProvider), ref.watch(authStorageProvider)),
);
