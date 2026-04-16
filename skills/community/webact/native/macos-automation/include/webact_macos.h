#ifndef WEBACT_MACOS_H
#define WEBACT_MACOS_H

#include <stdint.h>

char *weba_macos_list_apps_json(void);
char *weba_macos_list_windows_json(int32_t pid);
char *weba_macos_find_json(int32_t pid, const char *query_json);
char *weba_macos_click_json(int32_t pid, const char *query_json);
void weba_macos_free_string(char *ptr);

#endif
