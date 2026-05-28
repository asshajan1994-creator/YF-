import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/api_client.dart';
import '../../shared/widgets/async_view.dart';

final _opsProvider = FutureProvider.autoDispose<List<Map<String, dynamic>>>((ref) async {
  final api = ref.watch(apiClientProvider);
  final list = await api.get<List<dynamic>>('/operations');
  return list.cast<Map<String, dynamic>>();
});

final _dateFmt = DateFormat('d MMM');

class OperationsScreen extends ConsumerWidget {
  const OperationsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final value = ref.watch(_opsProvider);
    return AsyncView<List<Map<String, dynamic>>>(
      value: value,
      onRefresh: () => ref.refresh(_opsProvider.future),
      empty: const EmptyState(
        icon: Icons.agriculture_outlined,
        title: 'No operations scheduled',
        subtitle: 'Schedule plowing, sowing, irrigation and more',
      ),
      data: (ops) => ListView.separated(
        padding: const EdgeInsets.all(16),
        itemCount: ops.length,
        separatorBuilder: (_, __) => const SizedBox(height: 10),
        itemBuilder: (_, i) {
          final o = ops[i];
          final status = o['status'] as String;
          return Card(
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: _statusColor(context, status).withOpacity(0.15),
                child: Icon(_iconFor(o['operation_type'] as String),
                    color: _statusColor(context, status)),
              ),
              title: Text(
                (o['operation_type'] as String).replaceAll('_', ' '),
                style: const TextStyle(fontWeight: FontWeight.w600),
              ),
              subtitle: Text([
                if (o['scheduled_date'] != null)
                  'Scheduled ${_dateFmt.format(DateTime.parse(o['scheduled_date'] as String))}',
                if (o['assigned_to'] != null) 'Assigned: ${o['assigned_to']}',
              ].join(' · ')),
              trailing: Chip(
                label: Text(status.replaceAll('_', ' '), style: const TextStyle(fontSize: 11)),
                visualDensity: VisualDensity.compact,
                backgroundColor: _statusColor(context, status).withOpacity(0.12),
                side: BorderSide.none,
              ),
            ),
          );
        },
      ),
    );
  }

  IconData _iconFor(String type) {
    switch (type) {
      case 'plowing':
        return Icons.terrain;
      case 'sowing':
        return Icons.spa_outlined;
      case 'irrigation':
        return Icons.water_drop_outlined;
      case 'fertilization':
        return Icons.science_outlined;
      case 'pesticide':
        return Icons.bug_report_outlined;
      case 'weeding':
        return Icons.grass_outlined;
      case 'harvesting':
        return Icons.agriculture;
      default:
        return Icons.list_alt_outlined;
    }
  }

  Color _statusColor(BuildContext context, String status) {
    switch (status) {
      case 'completed':
        return Theme.of(context).colorScheme.primary;
      case 'in_progress':
        return Colors.orange;
      case 'cancelled':
        return Theme.of(context).colorScheme.error;
      default:
        return Theme.of(context).colorScheme.secondary;
    }
  }
}
