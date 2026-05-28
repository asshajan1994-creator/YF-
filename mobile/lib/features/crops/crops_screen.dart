import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/api_client.dart';
import '../../shared/widgets/async_view.dart';

final _cropsProvider = FutureProvider.autoDispose<List<Map<String, dynamic>>>((ref) async {
  final api = ref.watch(apiClientProvider);
  final list = await api.get<List<dynamic>>('/crops');
  return list.cast<Map<String, dynamic>>();
});

final _dateFmt = DateFormat('d MMM yyyy');

class CropsScreen extends ConsumerWidget {
  const CropsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final value = ref.watch(_cropsProvider);
    return AsyncView<List<Map<String, dynamic>>>(
      value: value,
      onRefresh: () => ref.refresh(_cropsProvider.future),
      empty: const EmptyState(
        icon: Icons.grass_outlined,
        title: 'No crops planned',
        subtitle: 'Crops you plan or sow will appear here',
      ),
      data: (crops) => ListView.separated(
        padding: const EdgeInsets.all(16),
        itemCount: crops.length,
        separatorBuilder: (_, __) => const SizedBox(height: 10),
        itemBuilder: (_, i) {
          final c = crops[i];
          final stage = (c['growth_stage'] as String?) ?? 'planned';
          return Card(
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: _stageColor(context, stage).withOpacity(0.15),
                child: Icon(Icons.grass_outlined, color: _stageColor(context, stage)),
              ),
              title: Text(
                  '${c['crop_name']} ${c['variety'] == null ? '' : '· ${c['variety']}'}',
                  style: const TextStyle(fontWeight: FontWeight.w600)),
              subtitle: Text([
                if (c['sowing_date'] != null) 'Sown ${_dateFmt.format(DateTime.parse(c['sowing_date'] as String))}',
                if (c['expected_harvest_date'] != null)
                  'Harvest ~${_dateFmt.format(DateTime.parse(c['expected_harvest_date'] as String))}',
              ].join(' · ')),
              trailing: Chip(
                label: Text(stage, style: const TextStyle(fontSize: 11)),
                visualDensity: VisualDensity.compact,
                backgroundColor: _stageColor(context, stage).withOpacity(0.12),
                side: BorderSide.none,
              ),
            ),
          );
        },
      ),
    );
  }

  Color _stageColor(BuildContext context, String s) {
    switch (s) {
      case 'harvested':
      case 'maturity':
        return Theme.of(context).colorScheme.primary;
      case 'flowering':
      case 'fruiting':
        return Colors.orange;
      default:
        return Theme.of(context).colorScheme.secondary;
    }
  }
}
