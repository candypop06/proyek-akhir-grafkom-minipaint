import copy


class HistoryManager:

    def __init__(self, max_states=50):

        self.max_states = max_states

        self.undo_stack = []
        self.redo_stack = []

    def save_state(self, shapes):

        state = copy.deepcopy(shapes)

        self.undo_stack.append(state)

        if len(self.undo_stack) > self.max_states:
            self.undo_stack.pop(0)

        self.redo_stack.clear()

    def undo(self, current_shapes):

        if not self.undo_stack:
            return copy.deepcopy(current_shapes)

        self.redo_stack.append(
            copy.deepcopy(current_shapes)
        )

        state = self.undo_stack.pop()

        return copy.deepcopy(state)

    def redo(self, current_shapes):

        if not self.redo_stack:
            return copy.deepcopy(current_shapes)

        self.undo_stack.append(
            copy.deepcopy(current_shapes)
        )

        state = self.redo_stack.pop()

        return copy.deepcopy(state)

    def clear(self):

        self.undo_stack.clear()
        self.redo_stack.clear()

    def can_undo(self):

        return len(self.undo_stack) > 0

    def can_redo(self):

        return len(self.redo_stack) > 0

    def undo_count(self):

        return len(self.undo_stack)

    def redo_count(self):

        return len(self.redo_stack)

    def info(self):

        return {
            "undo": len(self.undo_stack),
            "redo": len(self.redo_stack)
        }