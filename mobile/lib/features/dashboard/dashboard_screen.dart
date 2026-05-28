import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/api_client.dart';
import '../../shared/widgets/async_view.dart';
import '../../shared/widgets/stat_tile.dart';

final _dashboardProvider = FutureProvider.autoDispose<Map<String, dynamic>>((ref) async {
  final api = ref.watch(apiClientProvider);
  return api.get<Map<String, dynamic>>('/dashboard');
});

final _currency = NumberFormat.currency(locale: 'en_IN', symbol: '₹', decimalDigits: 0);
final _dateFmt = DateFormat('d MMM');

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final value = ref.watch(_dashboardProvider);
    return AsyncView<Map<String, dynamic>>(
      value: value,
      onRefresh: () => ref.refresh(_dashboardProvider.future),
      data: (d) {
        final stats = d['stats'] as Map<String, dynamic>;
        final ops = (d['upcoming_operations'] as List).cast<Map<String, dynamic>>();
        final alerts = (d['alerts'] as List).cast<Map<String, dynamic>>();

        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            _Section(
              title: 'Today at a glance',
              child: GridView.count(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                crossAxisCount: 2,
                mainAxisSpacing: 10,
                crossAxisSpacing: 10,
                childAspectRatio: 2.4,
                children: [
                  StatTile(
                      label: 'TOTAL AREA',
                      value:
                          '${(stats['total_area_acres'] as num).toStringAsFixed(1)} ac',
                      icon: Icons.map_outlined),
                  StatTile(
                      label: 'ACTIVE CROPS',
                      value: '${stats['active_crops']}',
                      icon: Icons.grass_outlined),
                  StatTile(
                      label: 'LABOR',
                      value: '${stats['active_laborers']}',
                      icon: Icons.groups_outlined),
                  StatTile(
                      label: 'PENDING OPS',
                      value: '${stats['pending_operations']}',
                      icon: Icons.list_alt_outlined),
                ],
              ),
            ),
            const SizedBox(height: 16),
            _Section(
              title: 'This month',
              child: Column(
                children: [
                  StatTile(
                      label: 'REVENUE',
                      value: _currency.format(stats['monthly_revenue']),
                      icon: Icons.trending_up,
                      tone: Colors.green),
                  const SizedBox(height: 8),
                  StatTile(
                      label: 'EXPENSE',
                      value: _currency.format(stats['monthly_expense']),
                      icon: Icons.payments_outlined,
                      tone: Colors.orange),
                  const SizedBox(height: 8),
                  StatTile(
                      label: 'PROFIT',
                      value: _currency.format(stats['monthly_profit']),
                      icon: Icons.account_balance_wallet_outlined,
                      tone: (stats['monthly_profit'] as num) >= 0
                          ? Colors.green
                          : Theme.of(context).colorScheme.error),
                ],
              ),
            ),
            const SizedBox(height: 16),
            if (alerts.isNotEmpty)
              _Section(
                title: 'Alerts',
                child: Column(
                  children: [
                    for (final a in alerts) _AlertCard(alert: a),
                  ],
                ),
              ),
            const SizedBox(height: 16),
            _Section(
              title: 'Upcoming operations',
              child: Card(
                child: Column(
                  children: [
                    if (ops.isEmpty)
                      const Padding(
                        padding: EdgeInsets.all(20),
                        child: Text('No operations scheduled in the next 30 days.'),
                      )
                    else
                      for (var i = 0; i < ops.length; i++) ...[
                        if (i > 0) const Divider(height: 1),
                        ListTile(
                          leading: const CircleAvatar(child: Icon(Icons.event_outlined)),
                          title: Text(
                            (ops[i]['operation_type'] as String).replaceAll('_', ' '),
                            style: const TextStyle(fontWeight: FontWeight.w500),
                          ),
                          subtitle: Text(
                              '${ops[i]['field_name']} · ${ops[i]['scheduled_date'] == null ? '—' : _dateFmt.format(DateTime.parse(ops[i]['scheduled_date'] as String))}'),
                          trailing: Chip(
                              label: Text(
                                (ops[i]['status'] as String).replaceAll('_', ' '),
                                style: const TextStyle(fontSize: 11),
                              ),
                              visualDensity: VisualDensity.compact),
                        ),
                      ],
                  ],
                ),
              ),
            ),
          ],
        );
      },
    );
  }
}

class _Section extends StatelessWidget {
  const _Section({required this.title, required this.child});
  final String title;
  final Widget child;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(bottom: 8, left: 4),
          child: Text(title,
              style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600, letterSpacing: 0.3)),
        ),
        child,
      ],
    );
  }
}

class _AlertCard extends StatelessWidget {
  const _AlertCard({required this.alert});
  final Map<String, dynamic> alert;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final level = (alert['level'] as String?) ?? 'info';
    final color = level == 'critical'
        ? scheme.error
        : level == 'warning'
            ? Colors.orange
            : scheme.primary;
    return Card(
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: color.withOpacity(0.15),
          child: Icon(level == 'critical' ? Icons.error_outline : Icons.warning_amber_outlined,
              color: color),
        ),
        title: Text(alert['title'] as String,
            style: const TextStyle(fontWeight: FontWeight.w500)),
        subtitle: Text(alert['detail'] as String),
      ),
    );
  }
}
