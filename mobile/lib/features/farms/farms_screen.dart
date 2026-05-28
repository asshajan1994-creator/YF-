import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/api_client.dart';
import '../../shared/widgets/async_view.dart';

final _farmsProvider = FutureProvider.autoDispose<List<Map<String, dynamic>>>((ref) async {
  final api = ref.watch(apiClientProvider);
  final list = await api.get<List<dynamic>>('/farms');
  return list.cast<Map<String, dynamic>>();
});

final _numberFmt = NumberFormat.decimalPattern('en_IN');

class FarmsScreen extends ConsumerWidget {
  const FarmsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final value = ref.watch(_farmsProvider);
    return Scaffold(
      body: AsyncView<List<Map<String, dynamic>>>(
        value: value,
        onRefresh: () => ref.refresh(_farmsProvider.future),
        empty: const EmptyState(
          icon: Icons.map_outlined,
          title: 'No farms yet',
          subtitle: 'Tap + to add your first farm',
        ),
        data: (farms) => ListView.separated(
          padding: const EdgeInsets.all(16),
          itemCount: farms.length,
          separatorBuilder: (_, __) => const SizedBox(height: 10),
          itemBuilder: (_, i) {
            final f = farms[i];
            return Card(
              child: ListTile(
                leading: const CircleAvatar(child: Icon(Icons.map_outlined)),
                title: Text(f['name'] as String,
                    style: const TextStyle(fontWeight: FontWeight.w600)),
                subtitle: Text([
                  if (f['district'] != null) f['district'],
                  if (f['state'] != null) f['state'],
                ].whereType<String>().join(', ')),
                trailing: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Text('${_numberFmt.format(f['total_area_acres'])} ac',
                        style: const TextStyle(fontWeight: FontWeight.w600)),
                    if (f['soil_type'] != null)
                      Text(f['soil_type'] as String,
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
        onPressed: () => _showAddFarmSheet(context, ref),
        icon: const Icon(Icons.add),
        label: const Text('Add farm'),
      ),
    );
  }

  void _showAddFarmSheet(BuildContext context, WidgetRef ref) {
    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      builder: (ctx) => _FarmForm(
        onSubmit: (data) async {
          await ref.read(apiClientProvider).post('/farms', body: data);
          ref.invalidate(_farmsProvider);
          if (ctx.mounted) Navigator.pop(ctx);
        },
      ),
    );
  }
}

class _FarmForm extends StatefulWidget {
  const _FarmForm({required this.onSubmit});
  final Future<void> Function(Map<String, dynamic>) onSubmit;

  @override
  State<_FarmForm> createState() => _FarmFormState();
}

class _FarmFormState extends State<_FarmForm> {
  final _formKey = GlobalKey<FormState>();
  final _name = TextEditingController();
  final _district = TextEditingController();
  final _location = TextEditingController();
  final _area = TextEditingController(text: '0');
  final _soil = TextEditingController();
  bool _saving = false;
  String? _error;

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _saving = true;
      _error = null;
    });
    try {
      await widget.onSubmit({
        'name': _name.text.trim(),
        'district': _district.text.trim(),
        'location': _location.text.trim(),
        'total_area_acres': double.tryParse(_area.text) ?? 0,
        'soil_type': _soil.text.trim().isEmpty ? null : _soil.text.trim(),
      });
    } catch (e) {
      if (mounted) setState(() => _error = e.toString());
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final insets = MediaQuery.of(context).viewInsets;
    return Padding(
      padding: EdgeInsets.fromLTRB(20, 20, 20, 20 + insets.bottom),
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text('New farm',
                style: TextStyle(fontWeight: FontWeight.w600, fontSize: 18)),
            const SizedBox(height: 16),
            TextFormField(
              controller: _name,
              decoration: const InputDecoration(labelText: 'Farm name'),
              validator: (v) => (v == null || v.trim().isEmpty) ? 'Required' : null,
            ),
            const SizedBox(height: 10),
            TextFormField(
              controller: _district,
              decoration: const InputDecoration(labelText: 'District'),
            ),
            const SizedBox(height: 10),
            TextFormField(
              controller: _location,
              decoration: const InputDecoration(labelText: 'Location / village'),
            ),
            const SizedBox(height: 10),
            TextFormField(
              controller: _area,
              keyboardType: const TextInputType.numberWithOptions(decimal: true),
              decoration: const InputDecoration(labelText: 'Total area (acres)'),
            ),
            const SizedBox(height: 10),
            TextFormField(
              controller: _soil,
              decoration: const InputDecoration(
                  labelText: 'Soil type', hintText: 'Red loam, Black cotton, Alluvial...'),
            ),
            if (_error != null) ...[
              const SizedBox(height: 10),
              Text(_error!, style: TextStyle(color: Theme.of(context).colorScheme.error)),
            ],
            const SizedBox(height: 18),
            FilledButton(
              onPressed: _saving ? null : _submit,
              child: _saving
                  ? const SizedBox(
                      width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2))
                  : const Text('Create farm'),
            ),
          ],
        ),
      ),
    );
  }
}
