// Created based on https://docs.rollbar.com/docs/webhooks

const STATUSES_COLORS = {
  green: '#2faa60',
  red: '#d22852',
  blue: '#607d8b',
};

class Script {

  process_incoming_request({ request }) {
    try {
      let result = null;
      const event_type = request.content.event_name;
      switch (event_type) {
        case 'exp_repeat_item':
          result = this.event_exp_repeat_item(request.content);
          break;
        case 'deploy':
          result = this.event_deploy(request.content);
          break;
        case 'item_velocity':
          result = this.event_item_velocity(request.content);
          break;
        case 'new_item':
          result = this.event_new_item(request.content);
          break;
        case 'occurrence':
        case 'reactivated_item':
          result = this.event_reactivated_item(request.content);
          break;
        case 'reopened_item':
        case 'resolved_item':
          result = this.event_resolved_item(request.content);
          break;
        default:
          result = null;
          break;
      }
      return result;
    } catch (e) {
      console.log('Rollbar Error', e);
      return this.createErrorChatMessage(e);
    }
  }

  createErrorChatMessage(error) {
    return {
      content: {
        text: `Error: '${error}', \n Message: '${error.message}', \n Stack: '${error.stack}'`,
        icon_url: null,
        attachments: []
      }
    };
  }

  event_exp_repeat_item(data) {
    var url = data.data.url;
    var title = data.data.item.title;
    var occurrences = data.data.item.total_occurrences;
    var environment = data.data.item.environment;
    return {
      content: {
        text: 'Occurrences threshold reached',
        icon_url: null,
        attachments: [
          {
            text: `Title: [${title}](${url}) \n Environment: ${environment} \n Occurrences: ${occurrences}`,
            color: STATUSES_COLORS['red']
          }
        ]
      }
    };
  }

  event_item_velocity(data) {
    var url = data.data.url;
    var title = data.data.item.title;
    var occurrences = data.data.item.total_occurrences;
    var environment = data.data.item.environment;
    var window_size = data.data.window_size;
    return {
      content: {
        text: 'Occurrence frequency threshold reached',
        icon_url: null,
        attachments: [
          {
            text: `Title: [${title}](${url}) \n Environment: ${environment} \n Occurrences: ${occurrences} \n Window Size: ${window_size}`,
            color: STATUSES_COLORS['red']
          }
        ]
      }
    };
  }

  event_new_item(data) {
    var url = data.data.url;
    var title = data.data.item.title;
    var environment = data.data.item.environment;
    return {
      content: {
        text: 'New item',
        icon_url: null,
        attachments: [
          {
            text: `Title: [${title}](${url}) \n Environment: ${environment}`,
            color: STATUSES_COLORS['red']
          }
        ]
      }
    };
  }

  event_reactivated_item(data) {
    var url = data.data.url;
    var title = data.data.item.title;
    var environment = data.data.item.environment;
    return {
      content: {
        text: 'Reactivated item',
        icon_url: null,
        attachments: [
          {
            text: `Title: [${title}](${url}) \n Environment: ${environment}`,
            color: STATUSES_COLORS['red']
          }
        ]
      }
    };
  }

  event_resolved_item(data) {
    var url = data.data.url;
    var title = data.data.item.title;
    var environment = data.data.item.environment;
    return {
      content: {
        text: 'Resolved item',
        icon_url: null,
        attachments: [
          {
            text: `Title: [${title}](${url}) \n Environment: ${environment}`,
            color: STATUSES_COLORS['green']
          }
        ]
      }
    };
  }

  event_deploy(data) {
    var url = `https://rollbar.com/deploy/${data.data.deploy.id}`
    var revision = data.data.deploy.revision;
    var environment = data.data.deploy.environment;
    var user = data.data.deploy.local_username;
    return {
      content: {
        text: 'New deployment',
        icon_url: null,
        attachments: [
          {
            text: `Revision: [${revision}](${url}) \n Environment: ${environment} \n Commited by: ${user}`,
            color: STATUSES_COLORS['green']
          }
        ]
      }
    };
  }
}
