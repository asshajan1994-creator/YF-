import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/api_client.dart';
import '../../shared/widgets/async_view.dart';
import '../../shared/widgets/stat_tile.dart';

final _txnsProvider = FutureProvider.autoDispose<List<Map<String, dynamic>>>((ref) async {
  final api = ref.watch(apiClientProvider);
  final list = await api.get<List<dynamic>>('/financial');
  return list.cast<Map<String, dynamic>>();
});

final _summaryProvider = FutureProvider.autoDispose<Map<String, dynamic>>((ref) async {
  final api = ref.watch(apiClientProvider);
  return api.get<Map<String, dynamic>>('/financial/summary');
});

final _currency = NumberFormat.currency(locale: 'en_IN', symbol: '₹', decimalDigits: 0);
final _dateFmt = DateFormat('d MMM');

class FinanceScreen extends ConsumerWidget {
  const FinanceScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final txns = ref.watch(_txnsProvider);
    final summary = ref.watch(_summaryProvider);

    return RefreshIndicator(
      onRefresh: () async {
        ref.invalidate(_txnsProvider);
        ref.invalidate(_summaryProvider);
        await Future.wait([
          ref.read(_txnsProvider.future),
          ref.read(_summaryProvider.future),
        ]);
      },
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          summary.when(
            data: (s) {
              final profit = (s['profit'] as num).toDouble();
              return Column(
                children: [
                  StatTile(
                      label: 'REVENUE',
                      value: _currency.format(s['revenue_total']),
                      icon: Icons.trending_up,
                      tone: Colors.green),
                  const SizedBox(height: 8),
                  StatTile(
                      label: 'EXPENSE',
                      value: _currency.format(s['expense_total']),
                      icon: Icons.payments_outlined,
                      tone: Colors.orange),
                  const SizedBox(height: 8),
                  StatTile(
                      label: 'PROFIT',
                      value: _currency.format(profit),
                      icon: Icons.account_balance_wallet_outlined,
                      tone: profit >= 0 ? Colors.green : Theme.of(context).colorScheme.error),
                ],
              );
            },
            loading: () => const SizedBox(
                height: 100, child: Center(child: CircularProgressIndicator())),
            error: (e, _) => Text('$e'),
          ),
          const SizedBox(height: 20),
          const Padding(
            padding: EdgeInsets.only(bottom: 8, left: 4),
            child: Text('Recent transactions',
                style:
                    TextStyle(fontSize: 13, fontWeight: FontWeight.w600, letterSpacing: 0.3)),
          ),
          txns.when(
            data: (rows) {
              if (rows.isEmpty) {
                return const Padding(
                  padding: EdgeInsets.symmetric(vertical: 40),
                  child: EmptyState(
                      icon: Icons.receipt_long_outlined, title: 'No transactions yet'),
                );
              }
              return Card(
                child: Column(
                  children: [
                    for (var i = 0; i < rows.length; i++) ...[
                      if (i > 0) const Divider(height: 1),
                      _TxnRow(rows[i]),
                    ],
                  ],
                ),
              );
            },
            loading: () => const Center(child: CircularProgressIndicator()),
            error: (e, _) => Text('$e'),
          ),
        ],
      ),
    );
  }
}

class _TxnRow extends StatelessWidget {
  const _TxnRow(this.t);
  final Map<String, dynamic> t;

  @override
  Widget build(BuildContext context) {
    final isRevenue = t['txn_type'] == 'revenue';
    final color = isRevenue ? Colors.green : Theme.of(context).colorScheme.error;
    return ListTile(
      leading: CircleAvatar(
        backgroundColor: color.withOpacity(0.12),
        child: Icon(isRevenue ? Icons.arrow_downward : Icons.arrow_upward, color: color),
      ),
      title: Text(
        (t['category'] as String).replaceAll('_', ' '),
        style: const TextStyle(fontWeight: FontWeight.w600),
      ),
      subtitle: Text([
        _dateFmt.format(DateTime.parse(t['txn_date'] as String)),
        if (t['counterparty'] != null) t['counterparty'],
        if (t['description'] != null) t['description'],
      ].whereType<String>().join(' · ')),
      trailing: Text(
        '${isRevenue ? '+' : '−'}${_currency.format(t['amount'])}',
        style: TextStyle(color: color, fontWeight: FontWeight.w600),
      ),
    );
  }
}
