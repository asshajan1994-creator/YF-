import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'auth_storage.dart';

class ApiClient {
  ApiClient(this._storage)
      : _dio = Dio(BaseOptions(
          baseUrl: _storage.apiUrl,
          connectTimeout: const Duration(seconds: 15),
          receiveTimeout: const Duration(seconds: 30),
        )) {
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) {
        final token = _storage.token;
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        handler.next(options);
      },
    ));
  }

  final AuthStorage _storage;
  final Dio _dio;

  Future<Map<String, dynamic>> login(String email, String password) async {
    final res = await _dio.post<Map<String, dynamic>>(
      '/auth/login',
      data: {'username': email, 'password': password},
      options: Options(contentType: Headers.formUrlEncodedContentType),
    );
    return res.data!;
  }

  Future<Map<String, dynamic>> register(Map<String, dynamic> payload) async {
    final res = await _dio.post<Map<String, dynamic>>('/auth/register', data: payload);
    return res.data!;
  }

  Future<Map<String, dynamic>> me() async {
    final res = await _dio.get<Map<String, dynamic>>('/auth/me');
    return res.data!;
  }

  Future<T> get<T>(String path, {Map<String, dynamic>? query}) async {
    final res = await _dio.get<T>(path, queryParameters: query);
    return res.data as T;
  }

  Future<T> post<T>(String path, {Object? body}) async {
    final res = await _dio.post<T>(path, data: body);
    return res.data as T;
  }

  Future<T> patch<T>(String path, {Object? body}) async {
    final res = await _dio.patch<T>(path, data: body);
    return res.data as T;
  }

  Future<void> delete(String path) async {
    await _dio.delete<void>(path);
  }
}

final apiClientProvider = Provider<ApiClient>(
  (ref) => ApiClient(ref.watch(authStorageProvider)),
);
