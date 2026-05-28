import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../features/auth/auth_provider.dart';
import '../features/auth/login_screen.dart';
import '../features/auth/register_screen.dart';
import '../features/crops/crops_screen.dart';
import '../features/dashboard/dashboard_screen.dart';
import '../features/farms/farms_screen.dart';
import '../features/finance/finance_screen.dart';
import '../features/inventory/inventory_screen.dart';
import '../features/labor/attendance_screen.dart';
import '../features/labor/labor_screen.dart';
import '../features/operations/operations_screen.dart';
import '../shared/widgets/app_scaffold.dart';

final routerProvider = Provider<GoRouter>((ref) {
  final auth = ref.watch(authProvider);
  return GoRouter(
    initialLocation: '/',
    refreshListenable: _AuthListenable(ref),
    redirect: (context, state) {
      final loggedIn = auth.isAuthenticated;
      final publicRoute = state.matchedLocation == '/login' || state.matchedLocation == '/register';
      if (auth.loading) return null;
      if (!loggedIn && !publicRoute) return '/login';
      if (loggedIn && publicRoute) return '/';
      return null;
    },
    routes: [
      GoRoute(path: '/login', builder: (_, __) => const LoginScreen()),
      GoRoute(path: '/register', builder: (_, __) => const RegisterScreen()),
      ShellRoute(
        builder: (context, state, child) => AppScaffold(location: state.matchedLocation, child: child),
        routes: [
          GoRoute(path: '/', builder: (_, __) => const DashboardScreen()),
          GoRoute(path: '/farms', builder: (_, __) => const FarmsScreen()),
          GoRoute(path: '/crops', builder: (_, __) => const CropsScreen()),
          GoRoute(path: '/operations', builder: (_, __) => const OperationsScreen()),
          GoRoute(
            path: '/labor',
            builder: (_, __) => const LaborScreen(),
            routes: [
              GoRoute(path: 'attendance', builder: (_, __) => const AttendanceScreen()),
            ],
          ),
          GoRoute(path: '/inventory', builder: (_, __) => const InventoryScreen()),
          GoRoute(path: '/finance', builder: (_, __) => const FinanceScreen()),
        ],
      ),
    ],
  );
});

class _AuthListenable extends ChangeNotifier {
  _AuthListenable(this._ref) {
    _ref.listen(authProvider, (_, __) => notifyListeners());
  }
  final Ref _ref;
}
