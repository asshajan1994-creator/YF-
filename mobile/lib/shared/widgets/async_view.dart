import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class AsyncView<T> extends StatelessWidget {
  const AsyncView({
    super.key,
    required this.value,
    required this.data,
    this.onRefresh,
    this.empty,
  });

  final AsyncValue<T> value;
  final Widget Function(T data) data;
  final Future<void> Function()? onRefresh;
  final Widget? empty;

  @override
  Widget build(BuildContext context) {
    return value.when(
      data: (d) {
        if (d is List && d.isEmpty && empty != null) {
          return RefreshIndicator(
            onRefresh: onRefresh ?? () async {},
            child: ListView(
              physics: const AlwaysScrollableScrollPhysics(),
              children: [
                const SizedBox(height: 80),
                Center(child: empty),
              ],
            ),
          );
        }
        if (onRefresh != null) {
          return RefreshIndicator(onRefresh: onRefresh!, child: data(d));
        }
        return data(d);
      },
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (e, _) => Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.error_outline, size: 36),
              const SizedBox(height: 8),
              Text(e.toString(), textAlign: TextAlign.center),
              const SizedBox(height: 12),
              if (onRefresh != null)
                FilledButton.tonal(onPressed: onRefresh, child: const Text('Retry')),
            ],
          ),
        ),
      ),
    );
  }
}

class EmptyState extends StatelessWidget {
  const EmptyState({super.key, required this.icon, required this.title, this.subtitle});
  final IconData icon;
  final String title;
  final String? subtitle;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, size: 48, color: scheme.onSurfaceVariant),
        const SizedBox(height: 10),
        Text(title, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 15)),
        if (subtitle != null) ...[
          const SizedBox(height: 4),
          Text(subtitle!, style: TextStyle(color: scheme.onSurfaceVariant)),
        ],
      ],
    );
  }
}
