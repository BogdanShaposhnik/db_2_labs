# messages statuses
STATUS_MESSAGE_CREATED = 'created'
STATUS_MESSAGE_ON_MODERATION = 'moderation'
STATUS_MESSAGE_BLOCKED = 'spam'
STATUS_MESSAGE_APPROVED = 'approve'
STATUS_MESSAGE_READ = 'read'

# roles
USER = 'user'
WORKER = 'worker'

# lists
LIST_ACTION_LOGS = 'actions-logs'

# sets
ONLINE_USERS_Z = 'online'
BLOCKED_MESSAGES_Z = 'spam'
APPROVED_MESSAGES_Z = 'approved'
ACTIVE_SENDERS_Z = 'active'
SPAMMERS_Z = 'top-spammers'
DELIVERED_MESSAGES_Z = 'delivered-messages'
READ_MESSAGES_Z = 'read-messages'
INCOMING_MESSAGES_Z = 'incoming_messages'
WAIT_FOR_MODERATION_MESSAGES_Z = 'wait-for-moderation-messages'
MESSAGES_ON_MODERATION_Z = 'on-moderation-messages'
SENT_MESSAGES_Z = 'sent-messages'

# sets
SET_WAIT_FOR_MODERATION = 'moderation-list'

# storage
MESSAGES_STORAGE = 'messages'
USERS_STORAGE = 'users'

# events
MESSAGE_CREATED_EVENT = 'msg-created'
MESSAGE_APPROVED_EVENT = 'message-approved'
INCOMING_MESSAGE_EVENT = 'incoming-message'
MESSAGE_BLOCKED_EVENT = 'blocked-message'
MESSAGE_READ_EVENT = 'read-message'