class Error(Exception):
    pass


class TaskDefinitionRelationError(Error):
    message = 'Task Definition always has to reference either a Checklist Definition or a Parent Task Definition'

    def __init__(self):
        super().__init__(self.message)


class TaskDefinitionMissingParentError(Error):
    message = 'The referenced TaskDefinition does not exist'

    def __init__(self):
        super().__init__(self.message)


class TaskDefinitionCircularReferenceError(Error):
    message = 'Circular Reference in TaskDefinition and its descendants is not allowed'

    def __init__(self):
        super().__init__(self.message)
