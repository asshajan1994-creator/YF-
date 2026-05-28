import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';

import '../../core/api_client.dart';
import '../../shared/widgets/async_view.dart';

final _laborProvider = FutureProvider.autoDispose<List<Map<String, dynamic>>>((ref) async {
  final api = ref.watch(apiClientProvider);
  final list = await api.get<List<dynamic>>('/labor');
  return list.cast<Map<String, dynamic>>();
});

final _currency = NumberFormat.currency(locale: 'en_IN', symbol: '₹', decimalDigits: 0);

class LaborScreen extends ConsumerWidget {
  const LaborScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final value = ref.watch(_laborProvider);
    return Scaffold(
      body: AsyncView<List<Map<String, dynamic>>>(
        value: value,
        onRefresh: () => ref.refresh(_laborProvider.future),
        empty: const EmptyState(
          icon: Icons.groups_outlined,
          title: 'No workers yet',
          subtitle: 'Add workers to track wages and attendance',
        ),
        data: (laborers) => ListView.separated(
          padding: const EdgeInsets.fromLTRB(16, 16, 16, 96),
          itemCount: laborers.length,
          separatorBuilder: (_, __) => const SizedBox(height: 10),
          itemBuilder: (_, i) {
            final l = laborers[i];
            return Card(
              child: ListTile(
                leading: CircleAvatar(
                  child: Text((l['full_name'] as String)
                      .split(' ')
                      .where((w) => w.isNotEmpty)
                      .take(2)
                      .map((w) => w[0].toUpperCase())
                      .join()),
                ),
                title: Text(l['full_name'] as String,
                    style: const TextStyle(fontWeight: FontWeight.w600)),
                subtitle: Text([
                  (l['labor_type'] as String).toUpperCase(),
                  if (l['phone'] != null) l['phone'],
                ].whereType<String>().join(' · ')),
                trailing: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Text(_currency.format(l['daily_wage']),
                        style: const TextStyle(fontWeight: FontWeight.w600)),
                    Text('/ day',
                        style: TextStyle(
                            fontSize: 11,
                            color: Theme.of(context).colorScheme.onSurfaceVariant)),
                  ],
                ),
              ),
            );
          },
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => context.go('/labor/attendance'),
        icon: const Icon(Icons.check_circle_outline),
        label: const Text('Mark attendance'),
      ),
    );
  }
}
