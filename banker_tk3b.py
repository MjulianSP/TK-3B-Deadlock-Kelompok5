#!/usr/bin/env python3
"""Simulasi Algoritma Banker untuk tugas TK-3B Sistem Operasi.

PENTING:
Angka Allocation, Max, dan Available di bawah adalah DATA SIMULASI.
Angka tersebut bukan data resmi kelas dari dosen. Ganti nilainya apabila
kelompok menerima matriks resmi.

Jalankan dari terminal VS Code:
    python3 src/banker_tk3b.py
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

RESOURCES = ["Kamera", "GPS", "Mikrofon", "Penyimpanan"]
PROCESSES = ["P1", "P2", "P3", "P4"]

# Urutan kolom: Kamera, GPS, Mikrofon, Penyimpanan.
ALLOCATION = [
    [1, 0, 0, 0],  # P1
    [0, 1, 0, 0],  # P2
    [0, 0, 1, 0],  # P3
    [1, 0, 0, 1],  # P4
]

MAX = [
    [1, 1, 0, 0],  # P1
    [1, 1, 1, 0],  # P2
    [0, 1, 1, 1],  # P3
    [1, 0, 1, 1],  # P4
]

AVAILABLE = [0, 1, 1, 1]


def validate_matrices(
    processes: Sequence[str],
    resources: Sequence[str],
    allocation: Sequence[Sequence[int]],
    maximum: Sequence[Sequence[int]],
    available: Sequence[int],
) -> None:
    """Memeriksa ukuran dan nilai matriks sebelum perhitungan dilakukan."""
    process_count = len(processes)
    resource_count = len(resources)

    if process_count == 0 or resource_count == 0:
        raise ValueError("Daftar proses dan resource tidak boleh kosong.")
    if len(allocation) != process_count or len(maximum) != process_count:
        raise ValueError("Jumlah baris Allocation dan Max harus sama dengan jumlah proses.")
    if len(available) != resource_count:
        raise ValueError("Jumlah nilai Available harus sama dengan jumlah jenis resource.")

    for matrix_name, matrix in (("Allocation", allocation), ("Max", maximum)):
        for row_index, row in enumerate(matrix):
            if len(row) != resource_count:
                raise ValueError(f"Baris {matrix_name} untuk {processes[row_index]} memiliki jumlah kolom yang salah.")
            if any(not isinstance(value, int) or value < 0 for value in row):
                raise ValueError(f"Nilai {matrix_name} harus berupa bilangan bulat nonnegatif.")

    if any(not isinstance(value, int) or value < 0 for value in available):
        raise ValueError("Available harus berisi bilangan bulat nonnegatif.")

    for i in range(process_count):
        for j in range(resource_count):
            if maximum[i][j] < allocation[i][j]:
                raise ValueError(
                    f"Max {processes[i]} untuk {resources[j]} tidak boleh lebih kecil daripada Allocation."
                )


def calculate_need(
    allocation: Sequence[Sequence[int]], maximum: Sequence[Sequence[int]]
) -> List[List[int]]:
    """Menghitung Need = Max - Allocation."""
    return [
        [maximum[i][j] - allocation[i][j] for j in range(len(maximum[i]))]
        for i in range(len(maximum))
    ]


def banker_safety_check(
    processes: Sequence[str],
    resources: Sequence[str],
    allocation: Sequence[Sequence[int]],
    maximum: Sequence[Sequence[int]],
    available: Sequence[int],
) -> Tuple[bool, List[str], List[str]]:
    """Mengembalikan status aman, safe sequence, dan proses yang belum selesai."""
    validate_matrices(processes, resources, allocation, maximum, available)
    need = calculate_need(allocation, maximum)
    work = list(available)
    finish = [False] * len(processes)
    safe_sequence: List[str] = []

    while len(safe_sequence) < len(processes):
        progress = False
        for i, process in enumerate(processes):
            if finish[i]:
                continue
            if all(need[i][j] <= work[j] for j in range(len(resources))):
                work = [work[j] + allocation[i][j] for j in range(len(resources))]
                finish[i] = True
                safe_sequence.append(process)
                progress = True
        if not progress:
            break

    unfinished = [processes[i] for i, done in enumerate(finish) if not done]
    return all(finish), safe_sequence, unfinished


def print_matrix(title: str, matrix: Sequence[Sequence[int]]) -> None:
    """Menampilkan matriks dengan nama proses dan resource."""
    print(f"\n{title}")
    print(f"{'Proses':<10}" + "".join(f"{resource:<16}" for resource in RESOURCES))
    for process, row in zip(PROCESSES, matrix):
        print(f"{process:<10}" + "".join(f"{value:<16}" for value in row))


def main() -> None:
    validate_matrices(PROCESSES, RESOURCES, ALLOCATION, MAX, AVAILABLE)
    need = calculate_need(ALLOCATION, MAX)

    print("=" * 72)
    print("SIMULASI ALGORITMA BANKER - TK-3B KELOMPOK 5")
    print("CATATAN: angka yang digunakan merupakan DATA SIMULASI/ILUSTRASI.")
    print("=" * 72)

    print_matrix("Matriks Allocation", ALLOCATION)
    print_matrix("Matriks Max", MAX)
    print_matrix("Matriks Need = Max - Allocation", need)
    print("\nAvailable awal:", dict(zip(RESOURCES, AVAILABLE)))

    safe, sequence, unfinished = banker_safety_check(
        PROCESSES, RESOURCES, ALLOCATION, MAX, AVAILABLE
    )

    print("\nHasil pemeriksaan:")
    if safe:
        print("Status: SAFE STATE")
        print("Safe sequence:", " -> ".join(sequence))
        print("Makna: terdapat urutan yang memungkinkan seluruh proses selesai.")
    else:
        print("Status: UNSAFE STATE")
        print("Proses yang belum dapat diselesaikan:", ", ".join(unfinished))
        print("Makna: sistem belum dapat menjamin seluruh proses selesai dengan aman.")


if __name__ == "__main__":
    main()
