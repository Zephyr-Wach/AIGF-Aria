# Aria v4.3 Proposal: Tiered Long-term Memory System

## 1. Design Philosophy

Optimized for **M4 chip performance** and **long-term stability**. This system employs "Importance-driven" non-linear memory management, prioritizing high information density over bulk storage.

## 2. Tiered Storage Architecture

| **Tier** | **Name**           | **Storage Media**   | **Lifespan**         | **Core Logic**                                               |
| -------- | ------------------ | ------------------- | -------------------- | ------------------------------------------------------------ |
| **L1**   | **Active Context** | RAM                 | 15-20 Rounds         | Sliding window; first 10 rounds distilled into a summary at 20-round limit. |
| **L2**   | **Fact Base**      | `facts.json` (SSD)  | Long-term (Weighted) | Importance scoring (1-10); JIT semantic retrieval injection. |
| **L3**   | **Deep Archive**   | `history.log` (SSD) | Permanent            | Append-only; full raw backup of all interactions.            |

------

## 3. L2 Fact Filtering & Injection Algorithm

### A. Static Core ($Score \ge 8$)

- **Content**: Environment preferences, long-term goals, persona definitions.
- **Handling**: Hard-coded into the System Prompt for every request.

### B. Semantic Association ($5 \le Score < 8$)

- **Content**: Sub-task status, specific bug logs, technical details.
- **Logic**: Triggered on-demand based on Keyword (Tag) matching from user input.

### C. Eviction & Downgrade Mechanism

- **Archiving**: Facts with low access frequency or expired TTL ($Score < 5$) are physically deleted from L2 and moved to L3.
- **Conflict Resolution**: Automatically overwrites old facts when new contradictory info arrives, while logging the change history.

------

## 4. 3-Year Vision: Digital Heritage

The L3 layer serves as a "Raw Black Box." It does not participate in real-time computation but provides a high-quality dataset for fine-tuning future models (e.g., on a Mac mini), ensuring a seamless "consciousness" migration.