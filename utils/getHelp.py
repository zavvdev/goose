from constants.actions import actions as act
from utils.styledText import styledText
from constants.textStyles import textStyles

# Name: getHelp
# Desc: Format help message
# Args: void
# Return: string

def getHelp():
  actStyle = textStyles["Bold"] + textStyles["White"]
  noteStyle = textStyles["Yellow"]
  note1 = styledText(noteStyle + "You can provide relative or absolute path for commands that uses it.")
  note2 = styledText(noteStyle + "You dont need to use double or single quotes to create/delete/upload/download file or directory with spaces in name.")
  note3 = styledText(noteStyle + "Put and Take actions move files to where you are at the moment. Example: \"put my-dir\" will upload my-dir folder in place where you in the remote server now.\n")
  rush = styledText(actStyle + act["Rush"])
  put = styledText(actStyle + act["Put"])
  take = styledText(actStyle + act["Take"])
  jump = styledText(actStyle + act["Jump"])
  delete = styledText(actStyle + act["Delete"])
  mkdir = styledText(actStyle + act["Mkdir"])
  cd = styledText(actStyle + act["Cd"])
  clear = styledText(actStyle + act["Clear"])
  ls = styledText(actStyle + act["Ls"])
  whereami = styledText(actStyle + act["WhereAmI"])
  whereamiShort = styledText(actStyle + act["WhereAmIShort"])
  whoami = styledText(actStyle + act["WhoAmI"])
  helpAct = styledText(actStyle + act["Help"])
  helpActShort = styledText(actStyle + act["HelpShort"])
  exit = styledText(actStyle + act["Exit"])
  exitShort = styledText(actStyle + act["ExitShort"])
  status = styledText(actStyle + act["Status"])
  return f"""
    {note1}
    {note2}
    {note3}
    {rush} example.ftp.com -- Connect to remote ftp server.
    {put} /local/path/to/data -- Upload file or directory to remote ftp server.
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
  