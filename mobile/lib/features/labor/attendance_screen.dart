import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/api_client.dart';

class AttendanceScreen extends ConsumerStatefulWidget {
  const AttendanceScreen({super.key});

  @override
  ConsumerState<AttendanceScreen> createState() => _AttendanceScreenState();
}

class _AttendanceScreenState extends ConsumerState<AttendanceScreen> {
  late Future<List<Map<String, dynamic>>> _future;
  DateTime _date = DateTime.now();
  final Map<int, _Entry> _entries = {};
  bool _saving = false;

  @override
  void initState() {
    super.initState();
    _future = _load();
  }

  Future<List<Map<String, dynamic>>> _load() async {
    final api = ref.read(apiClientProvider);
    final list = await api.get<List<dynamic>>('/labor');
    return list.cast<Map<String, dynamic>>().where((l) => l['is_active'] == true).toList();
  }

  Future<void> _save(List<Map<String, dynamic>> laborers) async {
    setState(() => _saving = true);
    final api = ref.read(apiClientProvider);
    try {
      for (final entry in _entries.entries) {
        if (!entry.value.present) continue;
        await api.post('/labor/attendance', body: {
          'laborer_id': entry.key,
          'work_date': DateFormat('yyyy-MM-dd').format(_date),
          'hours_worked': entry.value.hours,
          'task': entry.value.task.isEmpty ? null : entry.value.task,
          'wage_paid': 0,
        });
      }
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Saved ${_entries.values.where((e) => e.present).length} entries')),
      );
      setState(() {
        _entries.clear();
      });
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  Future<void> _pickDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: _date,
      firstDate: DateTime.now().subtract(const Duration(days: 30)),
      lastDate: DateTime.now().add(const Duration(days: 1)),
    );
    if (picked != null) setState(() => _date = picked);
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Map<String, dynamic>>>(
      future: _future,
      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return const Center(child: CircularProgressIndicator());
        }
        final laborers = snapshot.data!;
        final selected = _entries.values.where((e) => e.present).length;
        return Scaffold(
          appBar: AppBar(
            title: const Text('Attendance'),
            actions: [
              TextButton.icon(
                onPressed: _pickDate,
                icon: const Icon(Icons.calendar_today, size: 16),
                label: Text(DateFormat('d MMM').format(_date)),
              ),
            ],
          ),
          body: laborers.isEmpty
              ? const Center(child: Text('No active workers'))
              : ListView.separated(
                  padding: const EdgeInsets.fromLTRB(16, 16, 16, 100),
                  itemCount: laborers.length,
                  separatorBuilder: (_, __) => const SizedBox(height: 8),
                  itemBuilder: (_, i) {
                    final l = laborers[i];
                    final id = l['id'] as int;
                    final entry = _entries[id] ?? _Entry();
                    return Card(
                      child: Padding(
                        padding: const EdgeInsets.all(12),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Expanded(
                                  child: Text(l['full_name'] as String,
                                      style: const TextStyle(fontWeight: FontWeight.w600)),
                                ),
                                Switch(
                                  value: entry.present,
                                  onChanged: (v) {
                                    setState(() {
                                      _entries[id] = entry.copyWith(present: v);
                                    });
                                  },
                                ),
                              ],
                            ),
                            if (entry.present) ...[
                              const SizedBox(height: 8),
                              Row(
                                children: [
                                  Expanded(
                                    child: TextFormField(
                                      initialValue: entry.task,
                                      decoration: const InputDecoration(
                                        labelText: 'Task',
                                        isDense: true,
                                      ),
                                      onChanged: (v) {
                                        _entries[id] = entry.copyWith(task: v);
                                      },
                                    ),
                                  ),
                                  const SizedBox(width: 8),
                                  SizedBox(
                                    width: 80,
                                    child: TextFormField(
                                      initialValue: entry.hours.toString(),
                                      keyboardType: const TextInputType.numberWithOptions(
                                          decimal: true),
                                      decoration: const InputDecoration(
                                        labelText: 'Hrs',
                                        isDense: true,
                                      ),
                                      onChanged: (v) {
                                        final h = double.tryParse(v) ?? 8;
                                        _entries[id] = entry.copyWith(hours: h);
                                      },
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ],
                        ),
                      ),
                    );
                  },
                ),
          bottomNavigationBar: SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: FilledButton.icon(
                onPressed: _saving || selected == 0 ? null : () => _save(laborers),
                icon: _saving
                    ? const SizedBox(
                        width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                    : const Icon(Icons.check),
                label: Text(selected == 0
                    ? 'Mark workers present'
                    : 'Save attendance for $selected worker${selected == 1 ? '' : 's'}'),
              ),
            ),
          ),
        );
      },
    );
  }
}

class _Entry {
  _Entry({this.present = false, this.hours = 8.0, this.task = ''});
  bool present;
  double hours;
  String task;

  _Entry copyWith({bool? present, double? hours, String? task}) =>
      _Entry(present: present ?? this.present, hours: hours ?? this.hours, task: task ?? this.task);
}
