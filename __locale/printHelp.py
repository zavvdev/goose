from constants.actions import Actions as Act
from helpers.styledText import styledText
from constants.textStyles import textStyles

def printHelp():
  actStyle = textStyles["Bold"] + textStyles["White"]
  noteStyle = textStyles["Yellow"]
  note1 = styledText(noteStyle + "You can provide relative or absolute path for commands that uses it.")
  note2 = styledText(noteStyle + "You dont need to use double or single quotes to create/delete/upload/download file or directory with spaces in name.")
  note3 = styledText(noteStyle + "Drop and Take actions move files to where you are at the moment. Example: \"drop my-dir\" will upload my-dir folder in place where you in the remote server now.\n")
  rush = styledText(actStyle + Act["Rush"])
  drop = styledText(actStyle + Act["Drop"])
  take = styledText(actStyle + Act["Take"])
  jump = styledText(actStyle + Act["Jump"])
  delete = styledText(actStyle + Act["Delete"])
  mkdir = styledText(actStyle + Act["Mkdir"])
  cd = styledText(actStyle + Act["Cd"])
  clear = styledText(actStyle + Act["Clear"])
  ls = styledText(actStyle + Act["Ls"])
  whereami = styledText(actStyle + Act["WhereAmI"])
  whereamiShort = styledText(actStyle + Act["WhereAmIShort"])
  whoami = styledText(actStyle + Act["WhoAmI"])
  helpAct = styledText(actStyle + Act["Help"])
  helpActShort = styledText(actStyle + Act["HelpShort"])
  exit = styledText(actStyle + Act["Exit"])
  exitShort = styledText(actStyle + Act["ExitShort"])
  status = styledText(actStyle + Act["Status"])
  print(
    f"""
    {note1}
    {note2}
    {note3}
    {rush} example.ftp.com -- Connect to remote ftp server.
    {drop} /local/path/to/data -- Upload file or directory to remote ftp server.
    {take} /remote/path/to/data -- Download file or directory from remote ftp server.
    {jump} local -- Switch to local environment.
    {jump} remote -- Switch to remote environment.
    {status} -- Show connection status.
    {mkdir} /path/to/new/dir -- Create directory.
    {delete} /path/to/data -- Delete file or directory.
    {cd} /path/to/dir -- Change directory.
    {ls} -- Print list of content in current directory.
    {whereami} or {whereamiShort} -- Print current path.
    {whoami} -- Print your user name.
    {clear} -- Clear terminal.
    {helpAct} or {helpActShort} -- Print all available commands.
    {exit} or {exitShort} -- Terminate program.
    """
  )
  pass