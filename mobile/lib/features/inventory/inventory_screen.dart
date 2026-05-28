import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/api_client.dart';
import '../../shared/widgets/async_view.dart';

final _invProvider = FutureProvider.autoDispose<List<Map<String, dynamic>>>((ref) async {
  final api = ref.watch(apiClientProvider);
  final list = await api.get<List<dynamic>>('/inventory');
  return list.cast<Map<String, dynamic>>();
});

final _numberFmt = NumberFormat.decimalPattern('en_IN');
final _dateFmt = DateFormat('d MMM yyyy');

class InventoryScreen extends ConsumerWidget {
  const InventoryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final value = ref.watch(_invProvider);
    return AsyncView<List<Map<String, dynamic>>>(
      value: value,
      onRefresh: () => ref.refresh(_invProvider.future),
      empty: const EmptyState(
        icon: Icons.inventory_2_outlined,
        title: 'No inventory yet',
        subtitle: 'Track seeds, fertilizers, pesticides and tools',
      ),
      data: (items) => ListView.separated(
        padding: const EdgeInsets.all(16),
        itemCount: items.length,
        separatorBuilder: (_, __) => const SizedBox(height: 10),
        itemBuilder: (_, i) {
          final it = items[i];
          final qty = (it['quantity'] as num).toDouble();
          final reorder = (it['reorder_level'] as num).toDouble();
          final low = reorder > 0 && qty <= reorder;
          return Card(
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: low
                    ? Theme.of(context).colorScheme.errorContainer
                    : Theme.of(context).colorScheme.primaryContainer,
                child: Icon(
                  _iconFor(it['category'] as String),
                  color: low
                      ? Theme.of(context).colorScheme.error
                      : Theme.of(context).colorScheme.primary,
                ),
              ),
              title: Text(it['name'] as String,
                  style: const TextStyle(fontWeight: FontWeight.w600)),
              subtitle: Text([
                (it['category'] as String).replaceAll('_', ' '),
                if (it['expiry_date'] != null)
                  'exp ${_dateFmt.format(DateTime.parse(it['expiry_date'] as String))}',
              ].join(' · ')),
              trailing: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text('${_numberFmt.format(qty)} ${it['unit']}',
                      style: TextStyle(
                          fontWeight: FontWeight.w600,
                          color: low ? Theme.of(context).colorScheme.error : null)),
                  if (low)
                    Text('Low stock',
                        style: TextStyle(
                            fontSize: 11, color: Theme.of(context).colorScheme.error)),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  IconData _iconFor(String c) {
    switch (c) {
      case 'seed':
        return Icons.spa_outlined;
      case 'fertilizer':
        return Icons.science_outlined;
      case 'pesticide':
      case 'fungicide':
        return Icons.bug_report_outlined;
      case 'tool':
      case 'spare_part':
        return Icons.build_outlined;
      default:
        return Icons.inventory_2_outlined;
    }
  }
}
