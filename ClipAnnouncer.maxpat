{
  "patcher": {
    "fileversion": 1,
    "appversion": {
      "major": 9,
      "minor": 0,
      "revision": 10,
      "architecture": "x64",
      "modernui": 1
    },
    "classnamespace": "box",
    "rect": [
      60.0,
      120.0,
      820.0,
      460.0
    ],
    "openinpresentation": 1,
    "gridsize": [
      15.0,
      15.0
    ],
    "boxes": [
      {
        "box": {
          "hidden": 1,
          "id": "obj-1",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            24.0,
            18.0,
            220.0,
            20.0
          ],
          "text": "Clip Announcer (Phase 1)"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-2",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            24.0,
            52.0,
            80.0,
            20.0
          ],
          "text": "ANNOUNCE"
        }
      },
      {
        "box": {
          "id": "obj-3",
          "maxclass": "live.button",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "parameter_enable": 1,
          "patching_rect": [
            110.0,
            50.0,
            36.0,
            36.0
          ],
          "presentation": 1,
          "presentation_rect": [
            18.0,
            16.0,
            56.0,
            56.0
          ],
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_enum": [
                "off",
                "on"
              ],
              "parameter_longname": "announce_button",
              "parameter_mmax": 1,
              "parameter_modmode": 0,
              "parameter_shortname": "announce_button",
              "parameter_type": 2
            }
          },
          "varname": "announce_button"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-6",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            190.0,
            56.0,
            140.0,
            22.0
          ],
          "saved_object_attributes": {
            "filename": "clip_announcer.js",
            "parameter_enable": 0
          },
          "text": "js clip_announcer.js"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-7",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            344.0,
            56.0,
            260.0,
            22.0
          ],
          "saved_object_attributes": {
            "autostart": 1,
            "defer": 0,
            "node_bin_path": "",
            "npm_bin_path": "",
            "watch": 0
          },
          "text": "node.script clip_announcer_tts.js @autostart 1",
          "textfile": {
            "filename": "clip_announcer_tts.js",
            "flags": 0,
            "embed": 0,
            "autowatch": 1
          }
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-8",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 3,
          "outlettype": [
            "bang",
            "int",
            "int"
          ],
          "patching_rect": [
            24.0,
            110.0,
            90.0,
            22.0
          ],
          "text": "live.thisdevice"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-9",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            126.0,
            110.0,
            33.0,
            22.0
          ],
          "text": "init"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-10",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            171.0,
            110.0,
            79.0,
            22.0
          ],
          "text": "dump_state"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-12",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            262.0,
            110.0,
            72.0,
            22.0
          ],
          "text": "speak_test"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-11",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            24.0,
            160.0,
            620.0,
            20.0
          ],
          "text": "Selection state + summary logs are printed to the Max Console by clip_announcer.js"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-13",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 3,
          "outlettype": [
            "int",
            "int",
            "int"
          ],
          "patching_rect": [
            24.0,
            200.0,
            46.0,
            22.0
          ],
          "text": "notein"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-14",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "int",
            "int"
          ],
          "patching_rect": [
            80.0,
            200.0,
            62.0,
            22.0
          ],
          "text": "stripnote"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-15",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "bang",
            ""
          ],
          "patching_rect": [
            152.0,
            200.0,
            50.0,
            22.0
          ],
          "text": "sel 60"
        }
      }
    ],
    "lines": [
      {
        "patchline": {
          "destination": [
            "obj-6",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-10",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-7",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-12",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-6",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-3",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-7",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-6",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-9",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-8",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-6",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-9",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-14",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-13",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-14",
            1
          ],
          "hidden": 1,
          "source": [
            "obj-13",
            1
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-15",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-14",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-6",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-15",
            0
          ]
        }
      }
    ],
    "parameters": {
      "obj-3": [
        "announce_button",
        "announce_button",
        0
      ],
      "inherited_shortname": 1
    },
    "dependency_cache": [
      {
        "name": "clip_announcer.js",
        "bootpath": "~/Code Projects/Clip Announcer",
        "patcherrelativepath": ".",
        "type": "TEXT",
        "implicit": 1
      },
      {
        "name": "clip_announcer_tts.js",
        "bootpath": "~/Code Projects/Clip Announcer",
        "patcherrelativepath": ".",
        "type": "TEXT",
        "implicit": 1
      }
    ],
    "autosave": 0,
    "oscreceiveudpport": 0
  }
}
