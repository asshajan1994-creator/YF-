import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../features/auth/auth_provider.dart';

const _navItems = <_NavItem>[
  _NavItem('/', 'Dashboard', Icons.dashboard_outlined),
  _NavItem('/farms', 'Farms', Icons.map_outlined),
  _NavItem('/crops', 'Crops', Icons.grass_outlined),
  _NavItem('/operations', 'Operations', Icons.agriculture_outlined),
  _NavItem('/labor', 'Labor', Icons.groups_outlined),
  _NavItem('/inventory', 'Inventory', Icons.inventory_2_outlined),
  _NavItem('/finance', 'Finance', Icons.account_balance_wallet_outlined),
];

class _NavItem {
  const _NavItem(this.path, this.label, this.icon);
  final String path;
  final String label;
  final IconData icon;
}

class AppScaffold extends ConsumerWidget {
  const AppScaffold({super.key, required this.child, required this.location});
  final Widget child;
  final String location;

  String _titleFor(String loc) {
    final m = _navItems.firstWhere(
      (n) => loc == n.path || (n.path != '/' && loc.startsWith(n.path)),
      orElse: () => const _NavItem('/', 'Dashboard', Icons.dashboard),
    );
    return m.label;
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(authProvider).user;
    final scheme = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: AppBar(
        title: Text(_titleFor(location), style: const TextStyle(fontWeight: FontWeight.w600)),
        actions: [
          IconButton(
            onPressed: () => ref.read(authProvider.notifier).logout(),
            icon: const Icon(Icons.logout),
            tooltip: 'Log out',
          ),
        ],
      ),
      drawer: Drawer(
        child: SafeArea(
          child: Column(
            children: [
              DrawerHeader(
                margin: EdgeInsets.zero,
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(color: scheme.primaryContainer),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Container(
                      width: 44,
                      height: 44,
                      alignment: Alignment.center,
                      decoration: BoxDecoration(
                        color: scheme.primary,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Icon(Icons.grass, color: scheme.onPrimary),
                    ),
                    const SizedBox(height: 12),
                    Text('FarmBrain ERP',
                        style: TextStyle(
                            fontWeight: FontWeight.w700,
                            fontSize: 18,
                            color: scheme.onPrimaryContainer)),
                    const SizedBox(height: 2),
                    Text(
                      user?['full_name'] ?? 'User',
                      style: TextStyle(color: scheme.onPrimaryContainer.withOpacity(0.8)),
                    ),
                    Text(
                      (user?['role'] ?? '—').toString().toUpperCase(),
                      style: TextStyle(
                        color: scheme.onPrimaryContainer.withOpacity(0.7),
                        fontSize: 11,
                        letterSpacing: 1.2,
                      ),
                    ),
                  ],
                ),
              ),
              Expanded(
                child: ListView(
                  padding: const EdgeInsets.symmetric(vertical: 8),
                  children: [
                    for (final item in _navItems)
                      ListTile(
                        leading: Icon(item.icon),
                        title: Text(item.label),
                        selected: item.path == '/'
                            ? location == '/'
                            : location.startsWith(item.path),
                        selectedColor: scheme.primary,
                        onTap: () {
                          Navigator.of(context).pop();
                          context.go(item.path);
                        },
                      ),
                  ],
                ),
              ),
              const Divider(height: 1),
              Padding(
                padding: const EdgeInsets.all(16),
                child: Text('v0.1.0 · Tamil Nadu edition',
                    style: TextStyle(fontSize: 11, color: scheme.onSurfaceVariant)),
              ),
            ],
          ),
        ),
      ),
      body: child,
    );
  }
}
